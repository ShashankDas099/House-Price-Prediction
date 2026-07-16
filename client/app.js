const API_BASE = "https://house-price-prediction-model-1-ybt0.onrender.com";
let map;
let marker;
let trendChart;
let isRecording = false;
let recognition;

const PROPERTY_IMAGES = {
    unfurnished_1: "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=800&q=80",
    unfurnished_2: "https://images.unsplash.com/photo-1502005229762-cf1b2da7c5d6?auto=format&fit=crop&w=800&q=80",
    semi_1: "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?auto=format&fit=crop&w=800&q=80",
    semi_2: "https://images.unsplash.com/photo-1505691938895-1758d7feb511?auto=format&fit=crop&w=800&q=80",
    fully_1: "https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?auto=format&fit=crop&w=800&q=80",
    fully_2: "https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?auto=format&fit=crop&w=800&q=80"
};

// --- VOICE AI LOGIC ---
if ('webkitSpeechRecognition' in window) {
    recognition = new webkitSpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = true;

    recognition.onstart = function() {
        isRecording = true;
        document.getElementById("btnVoice").classList.add("recording");
        document.getElementById("voiceStatus").innerText = "Listening... speak now.";
        document.getElementById("voiceStatus").style.color = "#ef4444";
    };

    recognition.onresult = function(event) {
        let interimTranscript = '';
        let finalTranscript = '';
        for (let i = event.resultIndex; i < event.results.length; ++i) {
            if (event.results[i].isFinal) {
                finalTranscript += event.results[i][0].transcript;
            } else {
                interimTranscript += event.results[i][0].transcript;
            }
        }
        document.getElementById("voiceStatus").innerText = finalTranscript || interimTranscript;
        if (finalTranscript) processVoiceQuery(finalTranscript);
    };

    recognition.onerror = function(event) {
        document.getElementById("voiceStatus").innerText = "Error parsing voice. Please try again.";
        stopRecording();
    };

    recognition.onend = function() { stopRecording(); };
} else {
    document.getElementById("voiceStatus").innerText = "Voice Recognition not supported in this browser.";
}

function toggleVoice() {
    if(!recognition) { alert("Your browser does not support Speech Recognition. Try Google Chrome."); return; }
    if (isRecording) recognition.stop();
    else recognition.start();
}

function stopRecording() {
    isRecording = false;
    document.getElementById("btnVoice").classList.remove("recording");
    document.getElementById("voiceStatus").style.color = "#a78bfa";
}

function processVoiceQuery(query) {
    document.getElementById("voiceStatus").innerText = "Processing AI... '" + query + "'";
   $.post(API_BASE + "/api/nlp_parse", { query: query }, function(data) {
        document.getElementById("voiceStatus").innerText = "Magic Applied! ✨";
        if(data.bhk) $(`#bhk-${Math.min(data.bhk, 4)}`).prop('checked', true);
        if(data.sqft) $('#uiSqft').val(data.sqft);
        if(data.location) {
            $('#uiLocations').val(data.location).trigger('change');
            updateLocationOnMap();
        }
        if(data.furnishing !== null) {
            $('#uiFurnishing').val(data.furnishing);
            updatePropertyImage();
        }
        if(data.amenities) {
            $('.uiAmenity').prop('checked', false);
            if(data.amenities.amenity_swimming_pool) $('#cb_swimming_pool').prop('checked', true);
            if(data.amenities.amenity_gym) $('#cb_gym').prop('checked', true);
            if(data.amenities.amenity_garden) $('#cb_garden').prop('checked', true);
            if(data.amenities.amenity_security) $('#cb_security').prop('checked', true);
            if(data.amenities.amenity_parking) $('#cb_parking').prop('checked', true);
            if(data.amenities.amenity_club_house) $('#cb_club_house').prop('checked', true);
        }
        setTimeout(() => { onClickedEstimatePrice(); }, 800);
    });
}

// --- MAP LOGIC ---
function initMap() {
    map = L.map('map').setView([12.9716, 77.5946], 11);
    L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; OpenStreetMap', subdomains: 'abcd', maxZoom: 20
    }).addTo(map);
    marker = L.marker([12.9716, 77.5946]).addTo(map);
    createMockHeatmap();
}

function createMockHeatmap() {
    const coords = [
        { lat: 12.93, lng: 77.62, color: '#f43f5e', val: 'Expensive' }, // Koramangala
        { lat: 12.97, lng: 77.64, color: '#f43f5e', val: 'Expensive' }, // Indira Nagar
        { lat: 12.84, lng: 77.67, color: '#0ea5e9', val: 'Affordable' }, // Electronic City
        { lat: 13.09, lng: 77.59, color: '#0ea5e9', val: 'Affordable' }  // Yelahanka
    ];
    coords.forEach(c => {
        L.circle([c.lat, c.lng], { color: c.color, fillColor: c.color, fillOpacity: 0.2, radius: 3000 })
        .bindPopup(c.val + " Area").addTo(map);
    });
}

function updateLocationOnMap() {
    const loc = document.getElementById("uiLocations").value;
    loadMarketTrends(loc);
    
    const lat = 12.9716 + (Math.random() - 0.5) * 0.2;
    const lng = 77.5946 + (Math.random() - 0.5) * 0.2;
    map.flyTo([lat, lng], 13);
    marker.setLatLng([lat, lng]);
    
    document.getElementById("dist_school_km").value = (Math.random() * 2 + 0.5).toFixed(1);
    document.getElementById("dist_hospital_km").value = (Math.random() * 3 + 1).toFixed(1);
    document.getElementById("dist_bus_stop_km").value = (Math.random() * 1.5 + 0.1).toFixed(1);
    document.getElementById("dist_airport_km").value = (Math.random() * 20 + 20).toFixed(1);
}

// --- VISUALS & CHARTS ---
function updatePropertyImage() {
    const bhk = parseInt(getRadioValue("uiBHK"));
    const furnish = parseInt(document.getElementById("uiFurnishing").value);
    const imgEl = document.getElementById("propertyPreviewImg");
    
    let key = "semi_2";
    if(furnish === 0) key = bhk > 2 ? "unfurnished_2" : "unfurnished_1";
    if(furnish === 1) key = bhk > 2 ? "semi_2" : "semi_1";
    if(furnish === 2) key = bhk > 2 ? "fully_2" : "fully_1";
    
    imgEl.style.opacity = '0';
    setTimeout(() => {
        imgEl.src = PROPERTY_IMAGES[key] || PROPERTY_IMAGES["fully_1"];
        imgEl.style.opacity = '0.8';
    }, 300);
}

function loadMarketTrends(location) {
    $.get(API_BASE + "/api/market_trends?location=" + encodeURIComponent(location), function(data) {
        if(!data) return;
        const ctx = document.getElementById('trendChart').getContext('2d');
        if(trendChart) trendChart.destroy();
        
        trendChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: data.years,
                datasets: [{
                    label: 'Price Trend',
                    data: data.historical_prices,
                    borderColor: '#0ea5e9',
                    backgroundColor: 'rgba(14, 165, 233, 0.2)',
                    borderWidth: 3, tension: 0.4, fill: true
                }]
            },
            options: {
                responsive: true, maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: {
                    y: { grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#94a3b8', font: { family: 'monospace' } } },
                    x: { grid: { display: false }, ticks: { color: '#94a3b8', font: { family: 'monospace' } } }
                }
            }
        });
    });
}

function exportPDF() {
    const element = document.getElementById('reportWrapper');
    const opt = {
        margin: 10, filename: 'Property_Valuation_Report.pdf',
        image: { type: 'jpeg', quality: 0.98 },
        html2canvas: { scale: 2, useCORS: true, backgroundColor: '#09090b' },
        jsPDF: { unit: 'mm', format: 'a3', orientation: 'landscape' }
    };
    const btn = document.getElementById("exportBtn");
    const originalText = btn.innerHTML;
    btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Generating...';
    html2pdf().set(opt).from(element).save().then(() => { btn.innerHTML = originalText; });
}

// --- PREDICTION LOGIC ---
function getRadioValue(name) {
    const elements = document.getElementsByName(name);
    for(let i=0; i<elements.length; i++) {
        if(elements[i].checked) return elements[i].value;
    }
    return 2;
}

function onClickedEstimatePrice() {
    const btn = document.querySelector('.btn-predict');
    const originalBtnHtml = btn.innerHTML;
    btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing AI...';

   $.post(API_BASE + "/api/predict", {
        total_sqft: document.getElementById("uiSqft").value,
        bhk: getRadioValue("uiBHK"),
        bath: getRadioValue("uiBathrooms"),
        location: document.getElementById("uiLocations").value,
        furnishing_type: document.getElementById("uiFurnishing").value,
        amenities: Array.from(document.querySelectorAll('.uiAmenity:checked')).map(cb => cb.value).join(','),
        dist_school_km: document.getElementById("dist_school_km").value,
        dist_hospital_km: document.getElementById("dist_hospital_km").value,
        dist_airport_km: document.getElementById("dist_airport_km").value,
        dist_bus_stop_km: document.getElementById("dist_bus_stop_km").value
    }, function(data) {
        btn.innerHTML = originalBtnHtml;
        if(data && data.estimated_price) {
            document.getElementById("uiEstimatedPrice").innerText = data.estimated_price;
            document.getElementById("uiModelInfo").innerText = "Powered by " + (data.model_used || "AI");
            
            if(data.investment_insights) {
                document.getElementById("uiRent").innerText = "₹" + data.investment_insights.est_monthly_rent_inr.toLocaleString();
                document.getElementById("uiYield").innerText = data.investment_insights.rental_yield_percent + "%";
                document.getElementById("uiRating").innerText = data.investment_insights.rating;
            }
            
            document.getElementById("resultContainer").style.display = "block";
            document.getElementById("exportBtn").style.display = "block";
        }
    });
}

// --- INITIALIZATION ---
window.onload = function() {
    initMap();
    updatePropertyImage();
    
   $.get(API_BASE + "/api/locations", function(data) {
        if(data && data.locations) {
            const uiLocations = document.getElementById("uiLocations");
            $('#uiLocations').empty();
            $('#uiLocations').append(new Option("Select Location", "", true, true));
            data.locations.forEach(loc => { $('#uiLocations').append(new Option(loc, loc)); });
        }
    });
    
    loadMarketTrends("Electronic City");
};