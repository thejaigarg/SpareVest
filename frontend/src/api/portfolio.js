import API from "./client";

export async function getPortfolioSummary(){
    return API.get("/portfolio/summary")
        .then(r => r.data)
}