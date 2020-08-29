import axios from "redaxios";

export const Endpoint = {
  postFormSubmit: "/api/raffles/new",
  getSubmission: "/api/submission",
  getSubmissionsForCurrentUser: "/api/submissions",
  getJobStatus: "/api/job_status",
  getRafflesForUser: (username) => `/api/users/${username}/raffles`,
  showRaffle: (raffleId) => `/raffles/${raffleId}`,
  getRaffleMetrics: "/api/raffles/metrics",
  getRecentRaffles: "/api/raffles/recent",
};

/**
 * A simple wrapper to perform a GET and return the data as-is.
 * @param {*} endpoint
 */
export const getFromApi = async (endpoint) => {
  const { data } = await axios.get(endpoint);
  return data;
};
