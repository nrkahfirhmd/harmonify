function Footer() {
  return ( 
    <div className="flex justify-center items-center py-5 flex-col gap-3">
      <p className="highlight text-xl">
        &copy; 2025 Nurkahfi Amran Rahmada 
      </p>
      <div className="flex gap-2">
        <a href="">
          <img src="/images/github.png" alt="github" />
        </a>
        <a href="">
          <img src="/images/linkedin.png" alt="linkedin" />
        </a>
      </div>
    </div>
  );
}

export default Footer;