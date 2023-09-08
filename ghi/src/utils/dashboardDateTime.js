export const formatDateTime = (startDateTime, endDateTime) => {
  const startDateObj = new Date(startDateTime);
  const endDateObj = new Date(endDateTime);
  const options = {
    weekday: "short",
    month: "short",
    day: "numeric",
  };
  const removePrecedingZero = (timeStr) => timeStr.replace(/^0+/, "");

  const startDate = startDateObj
    .toLocaleDateString("en-US", options)
    .toLowerCase();
  const endDate = endDateObj.toLocaleDateString("en-US", options).toLowerCase();

  const formattedStartTime = removePrecedingZero(
    startDateObj.toLocaleTimeString("en-US", {
      hour: "2-digit",
      minute: "2-digit",
    })
  ).toLowerCase();
  const formattedEndTime = removePrecedingZero(
    endDateObj.toLocaleTimeString("en-US", {
      hour: "2-digit",
      minute: "2-digit",
    })
  ).toLowerCase();

  const startTimePeriod = formattedStartTime.slice(-2);
  const endTimePeriod = formattedEndTime.slice(-2);

  const startTime = formattedStartTime.slice(0, -3);
  const endTime = formattedEndTime.slice(0, -3);

  const displayTime =
    startTimePeriod === endTimePeriod
      ? `${startTime} - ${endTime} ${startTimePeriod}`
      : `${startTime} ${startTimePeriod} - ${endTime} ${endTimePeriod}`;

  return { startDate, startTime, endDate, endTime, displayTime };
};

// export const formatDateTime = (startTime, endTime) => {
//   const startDate = new Date(startTime);
//   const endDate = new Date(endTime);
//   const options = {
//     weekday: "short",
//     month: "short",
//     day: "numeric",
//     year: "numeric",
//   };
//   const removePrecedingZero = (timeStr) => timeStr.replace(/^0+/, "");

//   const formattedDate = startDate.toLocaleDateString("en-US", options);
//   const formattedStartTime = removePrecedingZero(
//     startDate.toLocaleTimeString("en-US", {
//       hour: "2-digit",
//       minute: "2-digit",
//     })
//   ).toLowerCase();
//   const formattedEndTime = removePrecedingZero(
//     endDate.toLocaleTimeString("en-US", {
//       hour: "2-digit",
//       minute: "2-digit",
//     })
//   ).toLowerCase();

//   const startTimePeriod = formattedStartTime.slice(-2);
//   const endTimePeriod = formattedEndTime.slice(-2);
//   const displayTime =
//     startTimePeriod === endTimePeriod
//       ? `${formattedStartTime.slice(0, -2)} - ${formattedEndTime}`
//       : `${formattedStartTime} - ${formattedEndTime}`;

//   return { formattedDate, displayTime };
// };
