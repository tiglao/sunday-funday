import React, { useEffect, useState } from "react";

function GoogleMap() {
  const [map, setMap] = useState(null);

  useEffect(() => {
    // Load the Google Maps API script dynamically
    const script = document.createElement("script");
    script.src = `https://maps.googleapis.com/maps/api/js?key=${process.env.REACT_APP_GOOGLE_MAPS_API_KEY}`;
    script.onload = initMap;
    document.head.appendChild(script);

    // Ensure the script is removed when the component unmounts
    return () => {
      document.head.removeChild(script);
    };
  }, []);

  const initMap = () => {
    // Initialize the map here

    // Example: Create a map centered at a default location
    const defaultLat = 38.897957;
    const defaultLng = -77.03656;
    const mapOptions = {
      center: { lat: defaultLat, lng: defaultLng },
      zoom: 8,
    };

    const newMap = new window.google.maps.Map(
      document.getElementById("map"),
      mapOptions
    );

    // Add markers, info windows, or other map features as needed
    // Example: Adding a marker at a specific location
    const marker = new window.google.maps.Marker({
      position: { lat: defaultLat, lng: defaultLng },
      map: newMap,
      title: "Marker Title",
    });

    // Set the map to state
    setMap(newMap);
  };

  return <div id="map" style={{ width: "100%", height: "400px" }}></div>;
}

export default GoogleMap;
