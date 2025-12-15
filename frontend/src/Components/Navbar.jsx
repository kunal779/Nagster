import { Link } from "react-router-dom";
import logo from "../assets/logo.svg";


export default function Navbar() {
  return (
    <header className="w-full flex justify-center bg-[#f7f5ef]">
      <div className="mt-4 w-full max-w-6xl flex items-center justify-between rounded-full bg-white px-6 py-3 shadow-sm">

        {/* Left: logo */}
        <div className="flex items-center gap-3">
          <img src={logo} alt="Nagster" className="h-8 w-8" />
        </div>

        {/* Center: links */}
        <nav className="hidden gap-8 text-sm font-medium text-neutral-700 md:flex">
          <a href="#home" className="hover:text-neutral-900">
            Home
          </a>
          <a href="#features" className="hover:text-neutral-900">
            Features
          </a>
          <a href="#download" className="hover:text-neutral-900">
            Agent
          </a>

          {/* This one is a real page */}
          <Link to="/docs" className="hover:text-neutral-900">
            Docs
          </Link>
        </nav>

        {/* Right: Login */}
        <div className="flex items-center gap-3">
          <Link
            to="/admin"
            className="rounded-full bg-black px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-neutral-900"
          >
            Admin Login
          </Link>
        </div>
      </div>
    </header>
  );
}
//test