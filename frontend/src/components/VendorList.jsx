import React,{useEffect, useState} from "react";
import api from "../api/apiClient";

export default function VendorList(){
  const [vendors,setVendors] = useState([]);
  const [loading,setLoading] = useState(true);

  useEffect(()=>{
    load();
  },[]);

  async function load(){
    setLoading(true);
    try{
      const res = await api.listVendors();
      setVendors(res.data || []);
    }catch(err){
      console.error(err);
    }finally{ setLoading(false); }
  }

  return (
    <div className="card">
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-lg font-semibold">Vendors</h3>
        <div className="text-sm text-muted">{vendors.length} total</div>
      </div>
      {loading ? <div>Loading...</div> : (
        <div className="overflow-auto">
          <table className="w-full text-left">
            <thead>
              <tr className="text-sm text-muted">
                <th className="py-2">Code</th>
                <th className="py-2">Name</th>
                <th className="py-2">Contact</th>
              </tr>
            </thead>
            <tbody>
              {vendors.map(v => (
                <tr key={v.code} className="border-t">
                  <td className="py-3">{v.code}</td>
                  <td className="py-3 font-medium">{v.name}</td>
                  <td className="py-3 text-sm text-muted">{v.contact_email || "-"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
