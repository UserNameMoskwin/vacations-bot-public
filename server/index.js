/**
 * Main server entry point - Telegram bot with cron scheduler.
 */
require('dotenv').config();
const { Telegraf } = require('telegraf');
const cron = require('node-cron');
const { spawn } = require('child_process');
const path = require('path');

// Configuration
const BOT_TOKEN = process.env.TELEGRAM_BOT_TOKEN;
const CHAT_ID = process.env.CHAT_ID;
const TIMEZONE = process.env.TIMEZONE || 'Europe/Moscow';

// Validate required env vars
if (!BOT_TOKEN) {
    console.error('Error: TELEGRAM_BOT_TOKEN is not set');
    process.exit(1);
}

if (!CHAT_ID) {
    console.error('Error: CHAT_ID is not set');
    process.exit(1);
}

// Initialize bot
const bot = new Telegraf(BOT_TOKEN);

/**
 * Execute Python script and get report.
 * @returns {Promise<{success: boolean, message?: string, error?: string}>}
 */
function generateReport() {
    return new Promise((resolve, reject) => {
        const pythonPath = process.platform === 'win32' ? 'python' : 'python3';
        const scriptPath = path.join(__dirname, '..', 'bot', 'bot.py');

        const python = spawn(pythonPath, [scriptPath], {
            cwd: path.join(__dirname, '..', 'bot')
        });

        let stdout = '';
        let stderr = '';

        python.stdout.on('data', (data) => {
            stdout += data.toString();
        });

        python.stderr.on('data', (data) => {
            stderr += data.toString();
        });

        python.on('close', (code) => {
            if (code !== 0) {
                reject(new Error(`Python script exited with code ${code}: ${stderr}`));
                return;
            }

            try {
                const result = JSON.parse(stdout);
                resolve(result);
            } catch (e) {
                reject(new Error(`Failed to parse Python output: ${stdout}`));
            }
        });

        python.on('error', (err) => {
            reject(new Error(`Failed to start Python: ${err.message}`));
        });
    });
}

/**
 * Send report to Telegram chat.
 */
async function sendReport() {
    try {
        console.log(`[${new Date().toISOString()}] Generating report...`);

        const result = await generateReport();

        if (!result.success) {
            console.error('Report generation failed:', result.error);
            return;
        }

        await bot.telegram.sendMessage(CHAT_ID, result.message, { parse_mode: 'HTML' });
        console.log(`[${new Date().toISOString()}] Report sent successfully`);
    } catch (error) {
        console.error('Error sending report:', error.message);
    }
}

// Bot command: /report - manual report trigger
bot.command('report', async (ctx) => {
    // Check if message is from the configured chat
    const chatId = ctx.chat.id.toString();

    console.log(`[${new Date().toISOString()}] Manual report requested by chat ${chatId}`);

    try {
        const result = await generateReport();

        if (!result.success) {
            await ctx.reply(`Report generation error: ${result.error}`);
            return;
        }

        await ctx.reply(result.message, { parse_mode: 'HTML' });
    } catch (error) {
        await ctx.reply(`Error: ${error.message}`);
    }
});

// Bot command: /start
bot.command('start', (ctx) => {
    ctx.reply('Absence notification bot is running.\n\nCommands:\n/report - get absence report now');
});

// Bot command: /help
bot.command('help', (ctx) => {
    ctx.reply('Commands:\n/report - get absence report\n/start - bot information');
});

// Schedule: Monday-Friday at 10:00
// Cron format: minute hour day-of-month month day-of-week
cron.schedule('0 10 * * 1-5', () => {
    console.log(`[${new Date().toISOString()}] Scheduled report triggered`);
    sendReport();
}, {
    timezone: TIMEZONE
});

// Start bot
bot.launch()
    .then(() => {
        console.log('Bot started successfully');
        console.log(`Timezone: ${TIMEZONE}`);
        console.log(`Chat ID: ${CHAT_ID}`);
        console.log('Scheduled: Monday-Friday at 10:00');
        console.log('Commands: /report, /start, /help');
    })
    .catch((error) => {
        console.error('Failed to start bot:', error.message);
        process.exit(1);
    });

// Graceful shutdown
process.once('SIGINT', () => bot.stop('SIGINT'));
process.once('SIGTERM', () => bot.stop('SIGTERM'));
