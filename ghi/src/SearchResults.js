import React, { useState, useEffect } from 'react';
import { useParams } from "react-router-dom";
import { baseUrl } from './utils/config';

import { useNavigate } from 'react-router-dom';

function SearchResult(){
    const {partyplanid} = useParams();
    const[results, setResults] = useState([]);
    const [dataIsLoaded, setDataIsLoaded] = useState(false);
    const navigate = useNavigate();

    useEffect(() => {
    const fetchSearchAndCreateLocations = async () => {
        try {
            // Fetch search results
            const response = await fetch(`${baseUrl}/locations/${partyplanid}/search_nearby`);
            if (!response.ok) {
                throw new Error("Failed to fetch nearby searches");
            }
            const searchData = await response.json();
            setResults(searchData.locations);

            // Create locations based on search results
            for (const result of searchData.locations) {
                try {
                    const existingResponse = await fetch(
                        `${baseUrl}/locations/${result.place_id}`
                    );
                    if (existingResponse.ok) {
                        const existingLocation = await existingResponse.json();
                        if (existingLocation) {
                            console.log(
                                'Location with this place_id already exists:',
                                existingLocation
                            );
                            continue; // Skip this iteration and move to the next result
                        }
                    }

                    // Map the search result to a format compatible with your LocationCreate model
                    const locationData = {
                        // Map the necessary fields from result to your LocationCreate model fields
                        place_id: result.place_id,
                        // Add other fields as needed
                    };

                    const response = await fetch(`${baseUrl}/locations/`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify(locationData),
                    });

                    if (!response.ok) {
                        const errorData = await response.json(); // Log the response body
                        console.error('Error creating location:', errorData);
                        throw new Error('Failed to create location');
                    }

                    const createdLocation = await response.json();
                    console.log('Created location:', createdLocation);
                } catch (error) {
                    console.error('Error creating location:', error);
                }
            }

            // Map the created locations to the required format
            const searchedLocations = searchData.locations.map(result => ({
                place_id: result.place_id,
                // Add other fields as needed
            }));

            // Update the party plan with the newly created locations
            const partyPlanUpdateResponse = await fetch(`${baseUrl}/party_plans/${partyplanid}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ searched_locations: searchedLocations }),
            });

            if (!partyPlanUpdateResponse.ok) {
                const errorData = await partyPlanUpdateResponse.json();
                console.error('Error updating party plan:', errorData);
                throw new Error('Failed to update party plan');
            }

            const updatedPartyPlan = await partyPlanUpdateResponse.json();
            console.log('Updated party plan:', updatedPartyPlan);
        } catch (error) {
            console.error('Error:', error);
        }
        setDataIsLoaded(true);
    };

    // Call the combined function to fetch, create, and update
    fetchSearchAndCreateLocations();
}, [partyplanid]);
    useEffect(() => {
    // Redirect once data is loaded and conditions are met
    if (dataIsLoaded) {
      navigate(`/dashboard/party_plans/${partyplanid}`);
    }
  }, [dataIsLoaded]);

    console.log("2",results)
    return(
        <>
        <div className="container party-plan-detail">
        <h1>Generating potential party place ...</h1>
        </div>
        </>
    );
}
export default SearchResult;
