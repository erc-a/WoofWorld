# woofworld_backend/woofworld_backend/tweens.py

from pyramid.settings import aslist

def cors_tween_factory(handler, registry):
    """
    Tween factory untuk menangani CORS.
    Akan mengambil konfigurasi dari settings.ini.
    """
    # Ambil konfigurasi CORS dari settings
    # Default ke nilai yang cukup permisif jika tidak ada di settings
    allowed_origins = aslist(registry.settings.get('cors.allow_origin', '*'))
    allowed_methods = aslist(registry.settings.get('cors.allow_methods', 'GET, POST, PUT, DELETE, OPTIONS'))
    allowed_headers = aslist(registry.settings.get('cors.allow_headers', 'Content-Type, Authorization, X-Requested-With'))
    allow_credentials = registry.settings.get('cors.allow_credentials', 'true').lower() == 'true'
    max_age = registry.settings.get('cors.max_age', '3600')

    def cors_tween(request):
        # Tangani preflight request (OPTIONS)
        if request.method == 'OPTIONS':
            response = request.response
            # Set header CORS untuk preflight
            # Hanya set origin jika origin request ada di daftar yang diizinkan atau jika '*'
            request_origin = request.headers.get('Origin')
            if '*' in allowed_origins or (request_origin and request_origin in allowed_origins):
                response.headers['Access-Control-Allow-Origin'] = request_origin if request_origin and '*' not in allowed_origins else '*'
            
            response.headers['Access-Control-Allow-Methods'] = ', '.join(allowed_methods)
            response.headers['Access-Control-Allow-Headers'] = ', '.join(allowed_headers)
            if allow_credentials:
                response.headers['Access-Control-Allow-Credentials'] = 'true'
            response.headers['Access-Control-Max-Age'] = max_age
            return response # Langsung kembalikan response untuk preflight

        # Untuk request aktual (selain OPTIONS)
        try:
            response = handler(request)
        except Exception as e:
            # Jika terjadi exception sebelum response terbentuk, kita perlu buat response baru
            # agar bisa menambahkan header CORS, lalu re-raise exception
            # Ini penting jika ada exception view yang juga perlu header CORS
            response = request.response 
            request_origin = request.headers.get('Origin')
            if '*' in allowed_origins or (request_origin and request_origin in allowed_origins):
                response.headers.setdefault('Access-Control-Allow-Origin', request_origin if request_origin and '*' not in allowed_origins else '*')
            
            if allow_credentials:
                 response.headers.setdefault('Access-Control-Allow-Credentials', 'true')
            # Header lain seperti Exposed-Headers bisa ditambahkan di sini jika perlu
            # response.headers.setdefault('Access-Control-Expose-Headers', 'Content-Length, X-My-Custom-Header')
            raise # Re-raise exception agar ditangani oleh exception view Pyramid

        # Tambahkan header CORS ke response yang berhasil
        request_origin = request.headers.get('Origin')
        if '*' in allowed_origins or (request_origin and request_origin in allowed_origins):
            response.headers.setdefault('Access-Control-Allow-Origin', request_origin if request_origin and '*' not in allowed_origins else '*')

        if allow_credentials:
            response.headers.setdefault('Access-Control-Allow-Credentials', 'true')
        
        # Header lain seperti Exposed-Headers bisa ditambahkan di sini jika perlu
        # response.headers.setdefault('Access-Control-Expose-Headers', 'Content-Length, X-My-Custom-Header')
            
        return response
    return cors_tween

# Fungsi includeme untuk dipanggil oleh config.include('.tweens')
def includeme(config):
    # Tambahkan tween. Urutan bisa penting.
    # 'INGRESS' adalah marker untuk tween yang paling awal dijalankan untuk request masuk.
    # 'MAIN' adalah setelah routing tetapi sebelum view utama.
    # 'EXCVIEW' adalah marker untuk exception view tween.
    # Menempatkan 'over=INGRESS' atau sebelum tween routing biasanya baik untuk CORS preflight.
    # Atau menempatkan setelah handler utama untuk memodifikasi semua response, termasuk error.
    # pyramid.tweens.excview_tween_factory adalah yang menangani exception views.
    # Kita ingin CORS header ada bahkan pada error responses.
    config.add_tween('woofworld_backend.tweens.cors_tween_factory', 
                     over='pyramid.tweens.excview_tween_factory')