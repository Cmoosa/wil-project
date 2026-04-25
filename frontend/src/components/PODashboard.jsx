import React, { useState } from "react";
import api from "../api/apiClient";
import POCard from "./POCard";

export default function PODashboard(){
  const [poNumber,setPoNumber]=useState("");
  const [result,setResult]=useState(null);
  const [err,setErr]=useState("");
  const [loading,setLoading]=useState(false);

  const search = async () => {
    setLoading(true); setErr(""); setResult(null);
    try{
      const res = await api.getPO(poNumber);
      setResult(res.data);
    }catch(e){
      setErr(e.response?.data?.error || e.message || "Not found");
    }finally{ setLoading(false); }
  };

  return (
    <div className="card">
      <div className="flex gap-3 mb-4">
        <input value={poNumber} onChange={e=>setPoNumber(e.target.value)} placeholder="PO Number" className="flex-1 rounded-lg border border-gray-200 px-3 py-2" />
        <button onClick={search} className="rounded-lg bg-primary text-white px-4 py-2">Search</button>
      </div>
      {err && <div className="text-red-600 mb-3">{err}</div>}
      {result && <POCard result={result} />}
      {!result && <div className="text-sm text-muted">Search a PO to see details</div>}
    </div>
  );
}
