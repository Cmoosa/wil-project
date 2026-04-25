import React from "react";

export default function StatusCard({ result }){
  if(!result) return null;
  return (
    <div className="card mt-3">
      <div><strong>PO:</strong> {result.po_number}</div>
      <div><strong>Vendor:</strong> {result.vendor_code}</div>
      <div><strong>Status:</strong> {result.status}</div>
      <div><strong>Total:</strong> R {result.total_amount}</div>
    </div>
  );
}
