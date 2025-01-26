function Header() {
  return ( 
    <div className="flex justify-between items-center py-5">
        <div className="w-100">
            <img src="/logo.png" alt="logo" className="h-16" />
        </div>
        {/* <div className="text-[#74512D] font-bold text-2xl">
            nurkahfi061204
        </div> */}
        <div className="flex gap-5">
            <button className="bg-[#74512D] text-[#F8F4E1] text-md px-7 py-3 rounded-2xl font-bold">LOGIN</button>
            <button className="bg-[#74512D] text-[#F8F4E1] text-md px-7 py-3 rounded-2xl font-bold">REGISTER</button>
        </div>
    </div>
  );
}

export default Header;