import { Link } from "react-router-dom";

const TestSpa = () => {
  return (
    <div>
      <h1>This is a test page</h1>
      <Link to="/party_plan/new">New Party Plan</Link>
    </div>
  );
};

export default TestSpa;
