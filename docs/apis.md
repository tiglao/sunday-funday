# APIs

## Party Plan

- **Method**: `POST`, `GET`, `GET`, `PUT`, `DELETE`,
- **Path**: `/api/party_plan`, `/api/party_plans/<int:pk>`
  Input:

```json
{
  "username": "Billy1234",
  "notes": "Notes go here....",
  "date": "2022-02-22",
  "invitees": {
    "name": "id",
    "name": "id",
    "name": "id",
    "name": "id"
  },
  "startTime": "2022-02-22 14:30",
  "endTime": "2022-02-22 17:30",
  "partyStatus": "draft",
  "keywords": ["fun", "bar", "burgers"],
  "generalLocation": "Denver",
  "favoriteLocations": {
    "location name": "place_id",
    "location name": "place_id",
    "location name": "place_id",
    "location name": "place_id"
  },
  "description": "Description here ....",
  "image": "https://picsum.photos/200"
}
```

Output:

```json
{
	"id": "???"
	"username": "Billy1234",
	"notes": "Notes go here....",
	"date": "2022-02-22",
	"invitees": {
		"name": "id",
		"name": "id",
		"name": "id",
		"name": "id",
	},
	"startTime": "2022-02-22 14:30",
	"endTime": "2022-02-22 17:30",
	"partyStatus": "draft",
	"keywords": ["fun", "bar", "burgers"],
	"generalLocation": "Denver",
	"favoriteLocations": {
		"location name": "place_id",
		"location name": "place_id",
		"location name": "place_id",
		"location name": "place_id",
	},
	"description": "Description here ....",
	"image": "https://picsum.photos/200",
}
```

**PartyPlan** is a digital checklist for organizing events. Party planners can set parameters, invite friends, and describe their party's vibe with keywords in order to generate a map of potential venues. Party planners can interact with a PartyPlan by creating, editing, or sharing their party plan details with others, ensuring every invitee is on the same page.

## Invitation

- **Method**: `POST`, `GET`, `PUT`, `DELETE`
- **Path**: `/api/invitation/`, `/api/invitations/<int:pk>`
  Input:

```json
{
	"account_id": string,
	"rsvpStatus": bool
}
```

Output:

```json
{
	"id": string,
	"account_id": string,
	"rsvpStatus": bool
}
```

**Invitation** is a digital tool for managing event responses. Event hosts can send invites to attendees, linking them to a specific account. Attendees can interact with an Invitation by accepting or declining, ensuring the host knows their attendance status.

## Location

- **Method**: `POST`, `GET`, `PUT`, `DELETE`
- **Path**: `/api/location/`, `/api/locations/<int:pk>`
  Input:

```json
`{
    "place_id": "specific_place_identifier",
    "name": "Location Name",
    "address": "123 Location Street, City, Country",
    "type": "Type of Location (e.g., Restaurant, Park, Museum)",
    "category": "Specific Category (e.g., Italian, Botanical, Art)",
    "favoriteStatus": false,
    "notes": "Any additional notes about the location",
    "hoursOfOperation": {
        "Monday": "9am-5pm",
        "Tuesday": "9am-5pm",
        // ... other days
    },
    "website": "https://example-location-website.com",
    "image": "https://location-specific-image-url.com"
}`
```

Output:

```json
`{
    "id": "some_generated_uuid",
    "place_id": "specific_place_identifier",
    "name": "Location Name",
    "address": "123 Location Street, City, Country",
    "type": "Type of Location (e.g., Restaurant, Park, Museum)",
    "category": "Specific Category (e.g., Italian, Botanical, Art)",
    "favoriteStatus": false,
    "notes": "Any additional notes about the location",
    "hoursOfOperation": {
        "Monday": "9am-5pm",
        "Tuesday": "9am-5pm",
        // ... other days
    },
    "website": "https://example-location-website.com",
    "image": "https://location-specific-image-url.com"
}`
```

**Location** is a digital reference for venues. Party planners can identify places by name, address, type, and even specify keywords like "???" or "???". Users can interact with a Location by marking it as a favorite, adding personal notes, or checking its hours and website.

## Account

- Method: `GET`, `POST`, `PUT`, `DELETE`
- Path: `/api/accounts`, `/api/account/<int:pk>`
  Input:

```json
{
  "email": "user@example.com",
  "password": "secure_password_here",
  "first_name": "John",
  "last_name": "Doe",
  "date_of_birth": "1990-01-01",
  "avatar": "https://user-avatar-url.com",
  "user_name": "john_doe_90"
}
```

Output:

```json
{
  "email": "user@example.com",
  "password": "secure_password_here",
  "first_name": "John",
  "last_name": "Doe",
  "date_of_birth": "1990-01-01",
  "avatar": "https://user-avatar-url.com",
  "user_name": "john_doe_90",
  "id": "some_generated_uuid"
}
```

**Account** represents a user's profile on the platform, containing essential details such as name, email, and birthdate. Users utilize their Account to sign in, modify personal information, and adjust their avatar.

Last update: 2023 August 16
