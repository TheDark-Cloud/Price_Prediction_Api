document.addEventListener('DOMContentLoaded', function () {
  const form = document.getElementById('predict-form');
  const errorEl = document.getElementById('form-error');

  form.addEventListener('submit', async function (e) {
    e.preventDefault();
    errorEl.textContent = '';

    const fd = new FormData(form);
    // Build payload following your Features model types
    const payload = {
      area: Number(fd.get('area')),
      bedrooms: parseInt(fd.get('bedrooms'), 10),
      bathrooms: parseInt(fd.get('bathrooms'), 10),
      stories: parseInt(fd.get('stories'), 10),
      mainroad: fd.get('mainroad') === 'true',
      guestroom: fd.get('guestroom') === 'true',
      basement: fd.get('basement') === 'true',
      hotwaterheating: fd.get('hotwaterheating') === 'true',
      airconditioning: fd.get('airconditioning') === 'true',
      parking: parseInt(fd.get('parking'), 10),
      prefarea: fd.get('prefarea') === 'true',
      furnishingstatus: fd.get('furnishingstatus')
    };

    // Basic validation
    if (isNaN(payload.area) || isNaN(payload.bedrooms) || isNaN(payload.bathrooms) || isNaN(payload.stories) || isNaN(payload.parking)) {
      errorEl.textContent = 'Please provide valid numeric values for area, bedrooms, bathrooms, stories, and parking.';
      return;
    }

    // POST to backend. Adjust URL if your API runs on a different host/port (CORS may be needed)
    const ENDPOINT = '/api/predict';
    try {
      const resp = await fetch(ENDPOINT, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(payload)
      });

      if (!resp.ok) {
        const j = await resp.json().catch(()=>null);
        errorEl.textContent = (j && (j.error || j.message)) || `API error: ${resp.status}`;
        return;
      }

      const json = await resp.json();
      const store = {
        input: payload,
        predictions: json.predictions || [],
        model_version: json.model_version || null,
        accuracy: json.accuracy !== undefined ? json.accuracy : (json.r2 !== undefined ? json.r2 : null)
      };
      sessionStorage.setItem('prediction_result', JSON.stringify(store));
      window.location.href = 'result.html';
    } catch (err) {
      console.error(err);
      errorEl.textContent = 'Network error: could not reach prediction API';
    }
  });
});