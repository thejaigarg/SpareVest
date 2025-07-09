import API from "./client";

export async function listTransctions({limit=5, offset=0}={}){
    return API.get("transctions", {params: {limit, offset} })
        .then(r => (Array.isArray(r.data) ? r.data : []))
}