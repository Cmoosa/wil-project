import React from "react";

export default function POCard({ result }){
  if(!result) return null;
  return (
    <div className="card mt-4">
      <div className="flex justify-between items-start">
        <div>
          <div className="text-sm text-muted">Purchase Order</div>
          <div className="text-lg font-semibold">{result.po_number}</div>
          <div className="text-sm">{result.vendor_code}</div>
        </div>
        <div className="text-right">
          <div className="text-sm text-muted">Status</div>
          <div className="font-medium">{result.status}</div>
          <div className="mt-2 text-xl font-bold">R {result.total_amount}</div>
        </div>
      </div>
      <div className="mt-4">
        <div className="text-sm font-medium mb-2">Lines</div>
        <ul className="space-y-2">
          {result.lines?.map((l,i)=>(
            <li key={i} className="text-sm border rounded p-2 bg-gray-50">
              {l.description} — {l.qty} × R {l.unit_price}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
