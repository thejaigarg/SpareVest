export function getCurrencySymbol(currency = "USD"){
    switch (currency.toUpperCase()){
        case "USD": return "$";
        case "EUR": return "€";
        case "GBP": return "£";
        case "INR": return "₹";
        case "JPY": return "¥";
        case "AUD": return "A$";
        default: return currency
    }
}