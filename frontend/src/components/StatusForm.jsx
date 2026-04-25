import React, { useState } from "react";
import api from "../api/apiClient";

export default function StatusForm({ setResult }){
  const [poNumber, setPoNumber] = useState("");
  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState("");

  const handleSubmit = async e => {
    e.preventDefault();
    setLoading(true); setErrorMsg("");
    try{
      const res = await api.getPO(poNumber);
      setResult(res.data);
    }catch(err){
      setErrorMsg(err.response?.data?.error || err.message || "Network error");
    }finally{ setLoading(false); }
  };

  return (
    <form onSubmit={handleSubmit} className="card">
      <input className="w-full rounded-lg border border-gray-200 px-4 py-2 mb-3" placeholder="PO Number" value={poNumber} onChange={e=>setPoNumber(e.target.value)} />
      {errorMsg && <div className="text-red-600 mb-2">{errorMsg}</div>}
      <div className="flex justify-end">
        <button disabled={loading} className="rounded-lg bg-primary text-white px-4 py-2">{loading ? "Checking..." : "Check Status"}</button>
      </div>
    </form>
  );
}
