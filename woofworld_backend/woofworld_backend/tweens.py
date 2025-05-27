# woofworld_backend/woofworld_backend/tweens.py

from pyramid.settings import aslist

def cors_tween_factory(handler, registry):
    """
    Tween factory untuk menangani CORS.
    Akan mengambil konfigurasi dari settings.ini.
    """
    # Ambil konfigurasi CORS dari settings
    # Default ke nilai yang cukup permisif jika tidak ada di settings
    # Jika cors.allow_origin tidak ada di settings, defaultnya adalah 'http://localhost:5173'
    # Jika ingin mengizinkan semua, set cors.allow_origin = * di development.ini
    allowed_origins_setting = registry.settings.get('cors.allow_origin', 'http://localhost:5173')
    allowed_origins = aslist(allowed_origins_setting)
    
    allowed_methods_setting = registry.settings.get('cors.allow_methods', 'GET, POST, PUT, DELETE, OPTIONS')
    allowed_methods = aslist(allowed_methods_setting)
    
    allowed_headers_setting = registry.settings.get('cors.allow_headers', 'Content-Type, Authorization, X-Requested-With, Origin, Accept')
    allowed_headers = aslist(allowed_headers_setting)
    
    allow_credentials = registry.settings.get('cors.allow_credentials', 'true').lower() == 'true'
    max_age = registry.settings.get('cors.max_age', '3600')

    def cors_tween(request):
        # Lewati penanganan CORS untuk rute internal seperti debug toolbar
        if request.path.startswith('/_debug_toolbar/'):
            return handler(request)

        response_origin = None
        request_origin = request.headers.get('Origin')

        if request_origin:
            if '*' in allowed_origins:
                response_origin = '*'
            elif request_origin in allowed_origins:
                response_origin = request_origin
            # Untuk pengembangan lokal dengan port berbeda-beda, bisa tambahkan logika ini
            # Namun hati-hati jika production, lebih baik eksplisit.
            # elif any(origin_pattern.startswith('http://localhost:') and request_origin.startswith('http://localhost:') for origin_pattern in allowed_origins):
            #     response_origin = request_origin


        # Tangani preflight request (OPTIONS)
        if request.method == 'OPTIONS':
            response = request.response
            # Selalu respons 200 OK untuk preflight yang valid
            # Beberapa browser mungkin lebih ketat jika Origin tidak cocok atau tidak ada
            # tapi jika Origin ada dan diizinkan, kita set headernya
            if response_origin:
                response.headers['Access-Control-Allow-Origin'] = response_origin
                response.headers['Access-Control-Allow-Methods'] = ', '.join(allowed_methods)
                response.headers['Access-Control-Allow-Headers'] = ', '.join(allowed_headers)
                if allow_credentials:
                    response.headers['Access-Control-Allow-Credentials'] = 'true'
                response.headers['Access-Control-Max-Age'] = max_age
            else:
                # Jika origin tidak diizinkan, preflight harusnya tidak berhasil.
                # Namun, untuk menghindari error, kita bisa return 200 tanpa header CORS
                # atau biarkan Pyramid menghandelnya (mungkin jadi 403/404 default)
                # Memberi 200 OK adalah praktik umum untuk preflight.
                pass
            
            response.status_code = 200 # Pastikan 200 OK untuk OPTIONS
            return response

        # Untuk request aktual (selain OPTIONS)
        try:
            response = handler(request)
        except Exception as e:
            # Jika terjadi exception sebelum response terbentuk (misal di view sebelum return Response)
            # kita perlu buat response baru dari request.response agar bisa menambahkan header CORS.
            # Ini penting jika ada exception view yang juga perlu header CORS.
            # Jika exception view sudah membuat response sendiri, kita akan memodifikasinya.
            if not hasattr(request, 'response') or not request.response:
                 # Seharusnya request.response sudah ada, tapi untuk jaga-jaga
                from pyramid.response import Response as PyramidResponse
                response = PyramidResponse()
            else:
                response = request.response
            
            # Tambahkan header CORS juga untuk error response
            if response_origin:
                response.headers.setdefault('Access-Control-Allow-Origin', response_origin)
                if allow_credentials:
                    response.headers.setdefault('Access-Control-Allow-Credentials', 'true')
            raise # Re-raise exception agar ditangani oleh exception view Pyramid

        # Tambahkan header CORS ke response yang berhasil
        if response_origin:
            response.headers.setdefault('Access-Control-Allow-Origin', response_origin)
            if allow_credentials:
                response.headers.setdefault('Access-Control-Allow-Credentials', 'true')
        
        # Header lain seperti Exposed-Headers bisa ditambahkan di sini jika perlu
        # response.headers.setdefault('Access-Control-Expose-Headers', 'Content-Length, X-My-Custom-Header')
            
        return response
        
    return cors_tween # <--- PERBAIKAN UTAMA ADA DI SINI

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