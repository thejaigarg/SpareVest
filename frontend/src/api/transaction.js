import API from "./client";

export async function listTransactions({limit=5, offset=0}={}){
    return API.get("/transactions/", {params: {limit, offset} })
        .then(r => (Array.isArray(r.data) ? r.data : []))
}