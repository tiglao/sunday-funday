import React, { useState, useEffect } from 'react';
import { useParams } from "react-router-dom";
import { baseUrl } from './utils/config';

function SearchResult(){
    const {partyplanid} = useParams();
    const[results, setResults] = useState([])

    useEffect(() =>{
        const fetchSearch = async () => {
            try{
                const response = await fetch(
                    `${baseUrl}/locations/${partyplanid}/search_nearby`
                );
                console.log(response);
                if (!response.ok) {
                        throw new Error("Failed to fetch nearby searchs");
                }
                const searchData = await response.json();
                setResults(searchData.locations);
                console.log("this one",searchData.locations);
                console.log(results)
            } catch(error) {
                console.error("Error fetching adventure:", error);
            }
        };
        fetchSearch();
    },[partyplanid]);
    useEffect(() => {
        const createLocations = async () => {
        for (const result of results) {
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
        };
    createLocations();
  }, [results]);
    useEffect(() => {
    const addToSearched = async () => {
        try {
            // Map the created locations to the required format
            const searchedLocations = results.map(result => ({
                place_id: result.place_id,
                // Add other fields as needed
            }));

            // Update the party plan with the newly created locations
            const response = await fetch(`${baseUrl}/party_plans/${partyplanid}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ searched_locations: searchedLocations }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                console.error('Error updating party plan:', errorData);
                throw new Error('Failed to update party plan');
            }

            const updatedPartyPlan = await response.json();
            console.log('Updated party plan:', updatedPartyPlan);
        } catch (error) {
            console.error('Error updating party plan:', error);
        }
    };

    // Call addToSearched after creating locations
    addToSearched();
}, [results]);

    console.log("2",results)
    return(
        <>
        <h1>Searchs</h1>

        </>
    );
}
export default SearchResult;
