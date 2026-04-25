import React from "react";
import POCreate from "../components/POCreate";

export default function CreatePOPage(){
  return (
    <div>
      <h1 className="text-2xl font-semibold mb-4">Create Purchase Order</h1>
      <POCreate />
    </div>
  );
}
