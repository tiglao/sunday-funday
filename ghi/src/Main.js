import MainLogin from "./MainLogin";

function Main() {
  return (
    <div className="bg-dark">
      <div className=" container-xxl p-0 bg-white min-vh-100">
        <div className="curved-header text-center text-white">
          <h1 className="header-text p-3">sunday funday</h1>
        </div>
        <div>
          <MainLogin />
        </div>
      </div>
    </div>
  );
}

export default Main;
