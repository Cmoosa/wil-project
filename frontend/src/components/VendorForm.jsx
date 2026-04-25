import { useState } from "react";
import api from "../api/apiClient";

export default function VendorForm({ onCreated }) {
  const [code, setCode] = useState("");
  const [name, setName] = useState("");
  const [contact_email, setEmail] = useState("");
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  const submit = async (e) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      const res = await api.createVendor({
        code,
        name,
        contact_email,
      });

      setCode("");
      setName("");
      setEmail("");

      if (onCreated) onCreated(res.data);
    } catch (err) {
      console.error(err);

      if (err.response) {
        setError(err.response.data?.error || "Request failed");
      } else {
        setError("Cannot reach backend (check server)");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={submit} className="card space-y-4">
      <h2 className="text-lg font-semibold">Create Vendor</h2>

      <input
        value={code}
        onChange={(e) => setCode(e.target.value)}
        placeholder="VEND001"
        className="input"
        required
      />

      <input
        value={name}
        onChange={(e) => setName(e.target.value)}
        placeholder="Vendor name"
        className="input"
        required
      />

      <input
        value={contact_email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="Email"
        className="input"
      />

      {error && <p className="text-red-600 text-sm">{error}</p>}

      <button className="btn-primary" disabled={loading}>
        {loading ? "Creating..." : "Create Vendor"}
      </button>
    </form>
  );
}
