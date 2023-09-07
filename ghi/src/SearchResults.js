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

    console.log("2",results)
    return(
        <>
        <h1>Searchs</h1>

        </>
    );
}
export default SearchResult;
