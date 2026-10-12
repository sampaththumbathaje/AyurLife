import { useContext } from "react";
import { AuthContext } from "../context/AuthContext";

/**
 * useAuth
 * -------
 * Custom hook to access authentication context.
 *
 * Returns:
 * - user
 * - isAuthenticated
 * - loading
 * - login()
 * - logout()
 */
const useAuth = () => {
  const context = useContext(AuthContext);

  if (!context) {
    throw new Error(
      "useAuth must be used within an AuthProvider"
    );
  }

  return context;
};

export default useAuth;
