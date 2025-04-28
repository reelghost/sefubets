const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');
const csv = require('csv-parser');

function normalizePhoneNumber(phone) {
    phone = phone.replace(/\s+/g, '');
    if (phone.startsWith('+254')) {
        return '0' + phone.slice(4);
    }
    return phone;
}

async function resetPassword(page, phoneNumber) {
    const resetUrl = 'https://api.sofabets.com/api/auth/password_reset';
    const payload = { phoneNumber };
    // Wait 2 seconds
    await new Promise(res => setTimeout(res, 2000));
    const response = await page.evaluate(async (url, data) => {
        const r = await fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        });
        return r.json();
    }, resetUrl, payload);
    console.log('[RESET]', response.message);
}

async function register(page, phoneNumber) {
    const password = '50bob';
    const refUrl = 'https://www.sofabets.com?ref=680536a687038800299eaa39';
    // Step 1: Go to refUrl (GET)
    await page.goto(refUrl, { waitUntil: 'networkidle2' });
    // Step 1.5: Click the header Register button to open the modal
    await page.waitForSelector('button.Header_register__irG5v');
    await page.click('button.Header_register__irG5v');
    // Step 2: Fill the registration form
    await page.waitForSelector('input[name="phone"]');
    await page.type('input[name="phone"]', phoneNumber, {delay: 50});
    await page.type('input[name="password"]', password, {delay: 50});
    await page.type('input[name="confirmPassword"]', password, {delay: 50});

    // Attach the response listener BEFORE clicking the button
    function handleRegisterResponse(response) {
        if (
            response.url() === 'https://api.sofabets.com/api/auth/register' &&
            response.request().method() === 'POST'
        ) {
            response.json().then(body => {
                console.log(`[REG]`, body.message);
            });
            // Remove the listener after the first match to avoid duplicate logs
            page.off('response', handleRegisterResponse);
        }
    }
    page.on('response', handleRegisterResponse);

    // Click the button and wait
    await page.click('button[type="submit"].LoginRegisterModal_submitButton__tX2uS');
    await new Promise(res => setTimeout(res, 1000));

    await resetPassword(page, phoneNumber);

}

function readPhoneNumbersFromCsv(csvPath) {
    return new Promise((resolve, reject) => {
        const phoneNumbers = [];
        fs.createReadStream(csvPath)
            .pipe(csv())
            .on('data', (row) => {
                if (row.PhoneNumber) {
                    const norm = normalizePhoneNumber(row.PhoneNumber.trim());
                    phoneNumbers.push(norm);
                }
            })
            .on('end', () => {
                resolve(phoneNumbers);
            })
            .on('error', reject);
    });
}

(async () => {
    const csvFile = path.join(__dirname, 'contacts.csv');
    const phoneNumbers = await readPhoneNumbersFromCsv(csvFile);
    for (const number of phoneNumbers) {
        console.log('Processing', number);
        try {
            const browser = await puppeteer.launch({ headless: true });
            const page = await browser.newPage();
            await register(page, number);
            await browser.close();
        } catch (e) {
            console.error('Error processing', number, e);
        }
    }
})();
