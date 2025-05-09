import Link from "next/link";

const Navbar = () => {
  return (
    <nav className="bg-neutral-800 text-white p-4 flex justify-between">
      <Link href="/" className="text-xl font-bold">Google Email Downloader</Link>
      <div className="space-x-4">
        <Link href="/" className="text-align:center justify-center hover:underline ">Home</Link>
        <Link href="/auth" className="text-align:center justify-center hover:underline">Authentication</Link>
        <Link href="/help" className="text-align:center justify-center hover:underline">Help</Link>
      </div>
    </nav>
  );
};

export default Navbar;
