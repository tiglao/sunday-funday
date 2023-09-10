import React, { useState } from "react";
import axios from "axios";

function PartyInvitationForm() {
    const [recipientEmail, setRecipientEmail] = useState("");
    const [partyDate, setPartyDate] = useState("");
    const [partyTime, setPartyTime] = useState("");
    const [partyLocation, setPartyLocation] = useState("");

    const handleSubmit = async (e) => {
        e.preventDefault();

        try {
            await axios.post("/send-invitation", {
                recipient_email: recipientEmail,
                party_date: partyDate,
                party_time: partyTime,
                party_location: partyLocation,
            });
            alert("Party invitation sent successfully!");
        }   catch (error) {
            console.error("Error sending party invitation:", error);
            alert("Error sending party invitation.");
        }
    };

    return (
        <div className="container mt-5">
            <h2 className="mb-4">Send Party Invitation</h2>
            <form onSubmit={handleSubmit}>
                <div className="mb-3">
                    <label htmlFor="recipientEmail" className="form-label">
                        Recipient's Email:
                    </label>
                    <input
                        type="email"
                        className="form-control"
                        id="recipientEmail"
                        value={recipientEmail}
                        onChange={(e) => setRecipientEmail(e.target.value)}
                        required
                    />
                </div>
                <div className="mb-3">
                    <label htmlFor="partyDate" className="form-label">
                        Party Date:
                    </label>
                    <input
                        type="text"
                        className="form-control"
                        id="partyDate"
                        value={partyDate}
                        onChange={(e) => setPartyDate(e.target.value)}
                        required
                    />
                </div>
                <div className="mb-3">
                    <label htmlFor="partyTime" className="form-label">
                        Party Time:
                    </label>
                    <input
                        type="text"
                        className="form-control"
                        id="partyTime"
                        value={partyTime}
                        onChange={(e) => setPartyTime(e.target.value)}
                        required
                    />
                </div>
                <div className="mb-3">
                    <label htmlFor="partyLocation" className="form-label">
                        Party Location:
                    </label>
                    <input
                        type="text"
                        className="form-control"
                        id="partyLocation"
                        value={partyLocation}
                        onChange={(e) => setPartyLocation(e.target.value)}
                        required
                    />
                </div>
                <button type="submit" className="btn btn-primary">
                    Send Invitation
                </button>
            </form>
        </div>
    );
}

export default PartyInvitationForm;
