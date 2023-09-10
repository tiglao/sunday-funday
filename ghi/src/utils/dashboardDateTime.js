export const formatDateTime = (startDateTime, endDateTime, localDate) => {
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

  const displayTime =
    formattedStartTime.slice(-2) === formattedEndTime.slice(-2)
      ? `${formattedStartTime.slice(0, -3)} - ${formattedEndTime.slice(
          0,
          -3
        )} ${formattedStartTime.slice(-2)}`
      : `${formattedStartTime} - ${formattedEndTime}`;

  return {
    startDate,
    formattedStartTime,
    endDate,
    formattedEndTime,
    displayTime,
  };
};

// export const formatDateTime = (startDateTime, endDateTime, localDate) => {
//   const startDateObj = new Date(startDateTime);
//   const endDateObj = new Date(endDateTime);
//   const options = {
//     weekday: "short",
//     month: "short",
//     day: "numeric",
//   };
//   const removePrecedingZero = (timeStr) => timeStr.replace(/^0+/, "");

//   const startDate = startDateObj
//     .toLocaleDateString("en-US", options)
//     .toLowerCase();
//   const endDate = endDateObj.toLocaleDateString("en-US", options).toLowerCase();

//   const formattedStartTime = removePrecedingZero(
//     startDateObj.toLocaleTimeString("en-US", {
//       hour: "2-digit",
//       minute: "2-digit",
//     })
//   ).toLowerCase();
//   const formattedEndTime = removePrecedingZero(
//     endDateObj.toLocaleTimeString("en-US", {
//       hour: "2-digit",
//       minute: "2-digit",
//     })
//   ).toLowerCase();

//   const displayTime =
//     formattedStartTime.slice(-2) === formattedEndTime.slice(-2)
//       ? `${formattedStartTime.slice(0, -3)} - ${formattedEndTime.slice(0, -3)} ${formattedStartTime.slice(-2)}`
//       : `${formattedStartTime} - ${formattedEndTime}`;

//   return { startDate, formattedStartTime, endDate, formattedEndTime, displayTime };
// };
