const gpmfExtract = require('gpmf-extract');
const goproTelemetry = require(`gopro-telemetry`);
const fs = require('fs');
 
const file = fs.readFileSync('GS018422.mp4');
 
// ENTIRE JSON
 
gpmfExtract(file)
.then(extracted => {
goproTelemetry(extracted, {
}, telemetry => {
fs.writeFileSync('GS018422-full.json', JSON.stringify(telemetry));
console.log('Telemetry saved as JSON');
});
})
.catch(error => console.error(error));
 
// FILTERED RESULTS
 
gpmfExtract(file)
.then(extracted => {
goproTelemetry(extracted, {
GPS5Fix: 3,
GPS5Precision: 500,
WrongSpeed: 50
}, telemetry => {
fs.writeFileSync('GS018422-filtered.json', JSON.stringify(telemetry));
console.log('Telemetry saved as JSON');
});
})
.catch(error => console.error(error));


// SINGLE STREAM
 
gpmfExtract(file)
.then(extracted => {
goproTelemetry(extracted, {
stream: 'GPS5'
}, telemetry => {
fs.writeFileSync('GS018422-gps-only.json', JSON.stringify(telemetry));
console.log('Telemetry saved as JSON');
});
})
.catch(error => console.error(error));

// THREE STREAMS
 
gpmfExtract(file)
.then(extracted => {
goproTelemetry(extracted, {
stream: ['GPS5','ACCL','GRAV']
}, telemetry => {
fs.writeFileSync('GS018422-three-streams.json', JSON.stringify(telemetry));
console.log('Telemetry saved as JSON');
});
})
.catch(error => console.error(error));

// THREE STREAMS FILTERED
 
gpmfExtract(file)
.then(extracted => {
goproTelemetry(extracted, {
stream: ['GPS5','ACCL','GRAV'],
GPS5Fix: 3,
GPS5Precision: 500,
WrongSpeed: 50
}, telemetry => {
fs.writeFileSync('GS018422-three-streams-filtered.json', JSON.stringify(telemetry));
console.log('Telemetry saved as JSON');
});
})
.catch(error => console.error(error));