import { baseUrl } from "../utils/config";

export const dummyPartyPlans = [
  {
    id: "fc3d9ad1-6d96-4975-b8ec-1c191d26df2f",
    account_id: "123456789",
    created: "2023-09-06T16:09:10.327000",
    updated: "2023-09-06T23:54:46.034000",
    api_maps_location: [
      {
        geo: null,
        input: "New York, NY",
      },
    ],
    start_time: "2022-02-24T05:30:00",
    end_time: "2022-02-24T20:30:00",
    description: "UGH",
    image: "https://picsum.photos/201",
    party_status: "draft",
    invitations: [
      "b468a97c-7ef9-41cb-ac49-2a5f080efdad",
      "41ef13e1-69d9-49cf-9008-ef6143e568a2",
    ],
    keywords: ["party", "drinks", "dance"],
    searched_locations: null,
    favorite_locations: null,
    chosen_locations: null,
  },
];

export const dummyInvitations = [
  {
    id: "b468a97c-7ef9-41cb-ac49-2a5f080efdad",
    created: "2023-09-06T20:09:35.821000",
    updated: null,
    account: {
      id: "123e4567-e89b-12d3-a456-426614174001",
      fullname: "hello",
      email: "hel@lo.com",
    },
    party_plan_id: "fc3d9ad1-6d96-4975-b8ec-1c191d26df2f",
    rsvp_status: null,
    sent_status: null,
  },
  // Add more dummy invitations as needed
];

const getNestedProp = (obj, path) => {
  return path.split(".").reduce((acc, part) => acc && acc[part], obj);
};

export const fetchResource = async (resource, filterKey, filterValue) => {
  try {
    const response = await fetch(`${baseUrl}/${resource}/`);
    if (response.ok) {
      const data = await response.json();
      console.log("Fetched data before filtering:", data);

      // Filtering and mapping logic with getNestedProp
      const filteredData = data
        .filter((item) => {
          const nestedValue = getNestedProp(item, filterKey);

          // Diagnostic logs
          console.log(`Current item for ${resource}:`, item);
          console.log(`Current filterKey for ${resource}:`, filterKey);

          console.log(`Checking nestedValue for ${resource}:`, nestedValue);
          console.log(`Against filterValue for ${resource}:`, filterValue);

          return nestedValue === filterValue;
        })
        .map((item) => ({ ...item, type: resource }));

      console.log(`Filtered data for ${resource}:`, filteredData);

      return filteredData;
    }

    if (response.status === 404) {
      console.error("404 - Endpoint not found");
      return [];
    }

    if (response.status === 401) {
      console.error("401 - Unauthorized");
      return [];
    }
  } catch (error) {
    console.error("Network Error");
    return [];
  }
};

export const fetchData = async (accountId, accountEmail) => {
  try {
    console.log(`accountId: ${accountId}, accountEmail: ${accountEmail}`);
    const [plans, invites] = await Promise.all([
      fetchResource("party_plans", "account_id", accountId),
      fetchResource("invitations", "account.email", accountEmail),
    ]);

    return [...plans, ...invites];
  } catch (error) {
    console.error("Error in fetchData");
    return [];
  }
};
