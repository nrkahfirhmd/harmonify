function Main() {
  return ( 
    <div className="min-h-[75vh] flex justify-center items-center flex-col gap-5 w-full">
      <div className="bg-[#74512D] flex justify-center flex-col gap-10 w-[40em] p-10 rounded-[2em]">
        <h1 className="text-[#F8F4E1] font-bold text-6xl">LOGIN</h1>
        <div className="flex flex-col gap-5">
            <div className="flex gap-2 w-full justify-center flex-col">
                <label className="text-[#F8F4E1] text-xl font-bold" htmlFor="username">Username</label>
                <input type="text" placeholder="username" className="px-3 py-2 w-full rounded-[0.5em] bg-[#AF8F6F] placeholder:text-[#F8F4E1]/25 text-[#F8F4E1] focus:outline-2 focus:outline-[#F8F4E1]" />
            </div>
            <div className="flex gap-2 w-full justify-center flex-col">
                <label className="text-[#F8F4E1] text-xl font-bold" htmlFor="password">Password</label>
                <input type="text" name="password" placeholder="password" className="px-3 py-2 w-full rounded-[0.5em] bg-[#AF8F6F] placeholder:text-[#F8F4E1]/25 text-[#F8F4E1] focus:outline-2 focus:outline-[#F8F4E1]" />
            </div>
            <div className="flex gap-2 text-[#F8F4E1] font-bold text-xl">
                <input type="checkbox" name="remember-me" id="remember-me" className="w-5 bg-[#74512D] checked:bg-[#74512D] default:outline-[#F8F4E1]" />
                <label htmlFor="remember-me">Remember Me</label>
            </div>
        </div>
        <div className="flex flex-col w-full justify-center items-center gap-5">
            <button className="bg-[#AF8F6F] text-[#F8F4E1] text-lg px-3 py-2 rounded-[0.5em] w-1/3">LOGIN</button>
            <p className="text-[#F8F4E1]">
                Don't have an account? <a href="" className="text-[#F8F4E1] underline">Register</a>
            </p>
        </div>
      </div>
    </div>
  );
}

export default Main;