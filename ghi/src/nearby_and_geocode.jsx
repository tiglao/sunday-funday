import React, { Component } from 'react';

class GoogleMapsComponent extends Component {
  constructor(props) {
    super(props);
    this.mapRef = React.createRef();
    this.state = {
      map: null,
      places: [],
    };
  }

  componentDidMount() {
    // Load Google Maps script
    const script = document.createElement('script');
    script.src = `https://maps.googleapis.com/maps/api/js?key=API_KEY&libraries=places`;
    script.async = true;
    script.onload = this.initMap;
    document.head.appendChild(script);
  }

  initMap = () => {
    const center = { lat: 48.8566 N, lng: 2.3522 E }; 
    const map = new window.google.maps.Map(this.mapRef.current, {
      center,
      zoom: 15,
    });
    this.setState({ map });
  };

  searchNearbyPlaces = () => {
    const { map } = this.state;

    const service = new window.google.maps.places.PlacesService(map);

    const request = {
      location: map.getCenter(),
      radius: 1000,
      type: ['restaurant', 'cafe', 'bar'],
    };

    service.nearbySearch(request, (results, status) => {
      if (status === window.google.maps.places.PlacesServiceStatus.OK) {
        this.setState({ places: results });
      }
    });
  };

  render() {
    return (
      <div>
        <button onClick={this.searchNearbyPlaces}>Search Nearby Places</button>
        <div ref={this.mapRef} style={{ width: '100%', height: '400px' }}></div>
        <div>
          <h2>Nearby Places</h2>
          <ul>
            {this.state.places.map((place, index) => (
              <li key={index}>{place.name}</li>
            ))}
          </ul>
        </div>
      </div>
    );
  }
}

export default GoogleMapsComponent;
