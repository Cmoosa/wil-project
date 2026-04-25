import Nav from "./Nav";
import { Outlet } from "react-router-dom";

export default function Layout() {
  return (
    <div className="min-h-screen flex flex-col">
      <Nav />
      <main className="flex-1 p-6">
        <Outlet />
      </main>
    </div>
  );
}
