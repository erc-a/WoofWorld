import { createContext } from 'react';

export const createAuthContext = () => {
  const AuthContext = createContext(null);

  const BaseAuthProvider = ({ children }) => {
    return <AuthContext.Provider>{children}</AuthContext.Provider>;
  };

  return { AuthContext, BaseAuthProvider };
};
