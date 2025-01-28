function Header() {
  return ( 
    <div className="flex justify-center flex-col md:flex-row md:justify-between items-center py-3 md:py-5 gap-2">
        <img src="/images/logo.png" alt="logo" className="h-14 md:h-16" />
        {/* <div className="highlight md:ordinary md:font-bold text-sm md:text-2xl">
            nurkahfi061204
        </div> */}
        <div className="highlight md:ordinary md:font-bold text-sm md:text-2xl md:hidden">
            Not Logged In!
        </div>
        <div className="hidden md:flex gap-5">
            <button className="bg-[#74512D] text-[#F8F4E1] text-md px-7 py-3 rounded-2xl font-bold">LOGIN</button>
            <button className="bg-[#74512D] text-[#F8F4E1] text-md px-7 py-3 rounded-2xl font-bold">REGISTER</button>
        </div>
    </div>
  );
}

export default Header;