function Main() {
  return ( 
    <div className="min-h-[75vh] flex justify-center items-center flex-col gap-5 w-full">
      <div className='text-md md:text-xl font-bold'>
        Amplify your Musical Harmony!
      </div>
      <div className='flex w-full md:w-1/2 relative md:flex-row flex-col gap-3 justify-center items-center'>
        <input type="text" placeholder='search for songs...' className='w-full bg-[#74512D] text-sm px-4 py-3 md:px-6 md:py-4 rounded-[20em] md:text-lg text-[#F8F4E1] placeholder:text-[#F8F4E1]/25 outline outline-2 focus:outline-[#AF8F6F]' />
        <button className='w-1/3 md:w-1/6 bg-[#AF8F6F] px-2 py-2 text-sm md:px-6 md:py-4 rounded-[20em] md:text-lg font-bold md:absolute right-0 top-0'>SEARCH</button>
      </div>
    </div>
  );
}

export default Main;
