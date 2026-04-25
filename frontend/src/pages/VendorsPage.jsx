import React, { useState } from "react";
import VendorForm from "../components/VendorForm";
import VendorList from "../components/VendorList";

export default function VendorsPage(){
  const [refreshKey, setRefreshKey] = useState(0);
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-semibold">Vendors</h1>
      </div>
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-1"><VendorForm onCreated={()=>setRefreshKey(k=>k+1)} /></div>
        <div className="lg:col-span-2"><VendorList key={refreshKey} /></div>
      </div>
    </div>
  );
}
