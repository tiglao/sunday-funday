export const formatDateTime = (startTime, endTime) => {
  const startDate = new Date(startTime);
  const endDate = new Date(endTime);
  const options = {
    weekday: "short",
    month: "short",
    day: "numeric",
    year: "numeric",
  };
  const removePrecedingZero = (timeStr) => timeStr.replace(/^0+/, "");

  const formattedDate = startDate.toLocaleDateString("en-US", options);
  const formattedStartTime = removePrecedingZero(
    startDate.toLocaleTimeString("en-US", {
      hour: "2-digit",
      minute: "2-digit",
    })
  ).toLowerCase();
  const formattedEndTime = removePrecedingZero(
    endDate.toLocaleTimeString("en-US", {
      hour: "2-digit",
      minute: "2-digit",
    })
  ).toLowerCase();

  const startTimePeriod = formattedStartTime.slice(-2);
  const endTimePeriod = formattedEndTime.slice(-2);
  const displayTime =
    startTimePeriod === endTimePeriod
      ? `${formattedStartTime.slice(0, -2)} - ${formattedEndTime}`
      : `${formattedStartTime} - ${formattedEndTime}`;

  return { formattedDate, displayTime };
};
