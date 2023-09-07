import { useAuthContext } from "@galvanize-inc/jwtdown-for-react";
import { useNavigate } from "react-router-dom";
import { useEffect } from "react";

function UserDashboard() {
  const { token } = useAuthContext();
  const navigate = useNavigate();
  useEffect(() => {
    console.log("Current Context Value:", dashboardContextValue);
  }, [dashboardContextValue]);

  useEffect(() => {
    const fetchData = async () => {
      await fetchPlans();
      await fetchInvitations();
    };

    fetchData();
  }, []);

  useEffect(() => {
    setCurrentData([...partyPlans, ...invitations]);
  }, [partyPlans, invitations]);

  const renderComingUp = () => {
    if (currentData) {
      return currentData.map((item, index) => {
        let displayContent, partyPath, startTime, endTime, imageUrl;
        if (item.type === "partyPlan") {
          displayContent = item.description;
          partyPath = `/party_plans/${item.id}`;
          startTime = item.start_time;
          endTime = item.end_time;
          imageUrl = item.image;
        } else if (item.type === "invitation") {
          const asscPartyPlan = partyPlans.find(
            (plan) => plan.id === item.party_plan_id,
          );
          if (asscPartyPlan) {
            displayContent = asscPartyPlan.description;
            partyPath = `/party_plans/${item.party_plan_id}`;
            startTime = asscPartyPlan.start_time;
            endTime = asscPartyPlan.end_time;
            imageUrl = asscPartyPlan.image;
          }
        }
        const { formattedDate, displayTime } = formatDateTime(
          startTime,
          endTime,
        );

        return (
          <div
            className="col-lg-4 col-md-6 col-sm-12 coming-up-col"
            key={index}
            onClick={() => {
              console.log("Item ID before passing to handler:", item.id);
              handleComingUpArrow(item.id);
            }}
          >
            <div className="card coming-up-card rounded">
              <div
                className="coming-up-image rounded"
                style={{ backgroundImage: `url(${imageUrl})` }}
              ></div>
              <div className="card-body">
                <div
                  onClick={() => handleComingUpArrow(item.id)}
                  className="coming-up-arrow"
                >
                  <FaArrowUp style={{ transform: "rotate(45deg)" }} />
                </div>
                <p className="card-text coming-up-text">
                  <span className="one-line">
                    {formattedDate.toLowerCase()}
                  </span>
                </p>
              </div>
            </div>
            <div className="description-under-card">
              <span className="coming-up-time">
                {displayTime}
                <br />
              </span>
            </div>
          </div>
        );
      });
    }
  }, [token, navigate]);

  if (!token) {
    return null;
  };

  const renderWaiting = () => {
    const allWaiting = partyPlans.filter(
      (plan) =>
        plan.party_status === "draft" || plan.party_status === "share draft",
    );
    return allWaiting.map((item, index) => {
      const { formattedDate, displayTime } = formatDateTime(
        item.start_time,
        item.end_time,
      );

      return (
        <div className="card waiting-cards p-3 mb-3 ml-4" key={index}>
          <div
            className="card-body"
            style={{ padding: "0", paddingTop: "2px" }}
          >
            <div
              className="waiting-arrow"
              onClick={() => handleWaitingArrow(item.id)}
            >
              <FaArrowUp style={{ transform: "rotate(45deg)" }} />
            </div>
            <p className="card-text one-line">
              {item.description}
              <br />
              <span className="waiting-date-time">
                {formattedDate.toLowerCase()} | {displayTime}
              </span>
            </p>
          </div>
        </div>
      );
    });
  };

  return (
    <div>
      <h1>User Dashboard</h1>
    </div>
  );
}

export default UserDashboard;
