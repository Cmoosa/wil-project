import { useState } from "react";
import api from "../api/apiClient";
import { useNavigate, Link } from "react-router-dom";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const submit = async () => {
    try {
      const res = await api.login({ email, password });

      // STORE SESSION
      localStorage.setItem("token", res.data.token);
      localStorage.setItem("user", JSON.stringify(res.data.user));

      // ENTERPRISE LANDING PAGE
      navigate("/menu", { replace: true });

    } catch (err) {
      setError("Invalid credentials. Please try again.");
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-[var(--color-surface)]">
      <div className="card w-full max-w-md">
        <h1 className="text-xl font-semibold mb-4">Sign in</h1>

        {error && (
          <div className="mb-3 text-sm text-red-600">{error}</div>
        )}

        <input
          className="w-full mb-3 border rounded px-3 py-2"
          placeholder="Email"
          onChange={(e) => setEmail(e.target.value)}
        />

        <input
          type="password"
          className="w-full mb-4 border rounded px-3 py-2"
          placeholder="Password"
          onChange={(e) => setPassword(e.target.value)}
        />

        <button
          onClick={submit}
          className="w-full bg-primary text-white rounded py-2"
        >
          Sign in
        </button>

        <p className="text-sm mt-4 text-center">
          No account?{" "}
          <Link to="/signup" className="text-primary">
            Create one
          </Link>
        </p>
      </div>
    </div>
  );
}
