import React, { useState } from "react";
import api from "../api/apiClient";

const LineRow = ({ idx, line, onChange, onRemove }) => (
  <div className="flex gap-3 items-center">
    <input value={line.description} onChange={e => onChange(idx, {...line, description: e.target.value})} placeholder="Description" className="flex-1 rounded-lg border border-gray-200 px-3 py-2" />
    <input value={line.qty} onChange={e => onChange(idx, {...line, qty: Number(e.target.value)})} type="number" className="w-20 rounded-lg border border-gray-200 px-3 py-2" />
    <input value={line.unit_price} onChange={e => onChange(idx, {...line, unit_price: Number(e.target.value)})} type="number" className="w-28 rounded-lg border border-gray-200 px-3 py-2" />
    <button type="button" onClick={() => onRemove(idx)} className="text-red-600">Remove</button>
  </div>
);

export default function POCreate({ onCreated }){
  const [vendorCode,setVendorCode] = useState("");
  const [lines,setLines] = useState([{ description: "", qty: 1, unit_price: 0 }]);
  const [loading,setLoading] = useState(false);
  const [error,setError] = useState("");

  const changeLine = (i,newLine) => { const copy=[...lines]; copy[i]=newLine; setLines(copy); };
  const addLine = () => setLines([...lines,{ description:"", qty:1, unit_price:0 }]);
  const removeLine = i => setLines(lines.filter((_,idx)=>idx!==i));
  const total = lines.reduce((s,l)=> s + (Number(l.qty||0) * Number(l.unit_price||0)), 0);

  const submit = async e => {
    e.preventDefault();
    setError("");
    if(!vendorCode) return setError("Vendor code required");
    if(lines.length===0) return setError("Add at least one line");
    setLoading(true);
    try{
      const payload = { vendorCode, items: lines };
      const res = await api.createPO(payload);
      onCreated && onCreated(res.data);
      setVendorCode(""); setLines([{ description:"", qty:1, unit_price:0 }]);
    }catch(err){
      setError(err.response?.data?.error || err.message || "Failed to create PO");
    }finally{ setLoading(false); }
  };

  return (
    <form onSubmit={submit} className="card">
      <h3 className="text-lg font-semibold mb-3">Create Purchase Order</h3>
      <div className="space-y-3">
        <input value={vendorCode} onChange={e=>setVendorCode(e.target.value)} placeholder="Vendor Code" className="w-full rounded-lg border border-gray-200 px-4 py-2" />
        <div className="space-y-2">
          {lines.map((line,i)=> <LineRow key={i} idx={i} line={line} onChange={changeLine} onRemove={removeLine} />)}
        </div>
        <div className="flex items-center justify-between">
          <div className="text-sm text-muted">Total: <strong>R {total}</strong></div>
          <div className="flex gap-2">
            <button type="button" onClick={addLine} className="rounded-lg px-3 py-2 border border-gray-200">Add Line</button>
            <button disabled={loading} className="rounded-lg bg-primary text-white px-4 py-2">{loading ? "Creating..." : "Create PO"}</button>
          </div>
        </div>
        {error && <div className="text-red-600">{error}</div>}
      </div>
    </form>
  );
}
