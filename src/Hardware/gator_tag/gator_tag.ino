// Gatorball version of tag code. Currently this is similar to the examples but going forward this will be what is run and added to.
#include "dw3000.h"

#define PIN_RST 27
#define PIN_IRQ 34
#define PIN_SS 4
// Delay values for calculating rx time taken from vendor. Will be re-calibrated if necessary.
#define TX_ANT_DLY 16385
#define RX_ANT_DLY 16385
#define POLL_TX_TO_RESP_RX_DLY_UUS 240
#define RESP_RX_TIMEOUT_UUS 400

const dwt_config_t config {
    5, // chan
    DWT_PLEN_256, //txPreambLength
    DWT_PAC8, //rxPac
    9,
    9,
    1,
    DWT_BR_6M8,
    DWT_PHRMODE_STD,
    DWT_PHRRATE_STD,
    256 + 1 + 8 - 8,
    DWT_STS_MODE_OFF,
    0,
    DWT_PDOA_M0,
};

// tx and expected rx are from vendor. Need to see how much control we have over this formatting
static uint8_t tx_poll_msg[] = {0x41, 0x88, 0, 0xCA, 0xDE, 'W', 'A', 'V', 'E', 0xE0, 0, 0};
static uint8_t rx_resp_msg[] = {0x41, 0x88, 0, 0xCA, 0xDE, 'V', 'E', 'W', 'A', 0xE1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
static uint8_t rx_buffer[20];

void setup() {
    Serial.begin(115200);
    Serial.println("GatorBall Tag");

    spiBegin(PIN_IRQ, PIN_RST);
    spiSelect(PIN_SS);

    delay(2);
    while (!dwt_checkidlerc());
    Serial.println("IDLE_RC state entered");

    if (dwt_initialise(DWT_DW_INIT) == -1) {
        Serial.println("Init failed");
        while(1);
    } else {
        Serial.println("Initialized");
    }

    if (dwt_configure(&config) == -1) {
        Serial.println("Config failed");
        while(1);
    } else {
        Serial.println("Configured");
    }

    dwt_configuretxrf(&txconfig_options);
    dwt_setrxaftertxdelay(POLL_TX_TO_RESP_RX_DLY_UUS); // time to open rx buffer after tx
    dwt_setrxtimeout(RESP_RX_TIMEOUT_UUS);
    // See above
    dwt_setrxantennadelay(RX_ANT_DLY);
    dwt_settxantennadelay(TX_ANT_DLY);

    Serial.println("DWM3000 setup complete");

    btSerial.begin("Gatorball Tag");  //Bluetooth device name
    btSerial.connect();
    Serial.println("Bluetooth setup complete");

}

void loop() {

    // Initiate TX
    dwt_write32bitreg(SYS_STATUS_ID, SYS_STATUS_TXFRS_BIT_MASK);
    dwt_writetxdata(sizeof(tx_poll_msg), tx_poll_msg, 0);
    dwt_writetxfctrl(sizeof(tx_poll_msg), 0, 1);
    dwt_starttx(DWT_START_TX_IMMEDIATE | DWT_RESPONSE_EXPECTED);

    // poll for rx or timeout
    uint32_t status_reg;
    while (!((status_reg = dwt_read32bitreg(SYS_STATUS_ID)) & (SYS_STATUS_RXFCG_BIT_MASK | SYS_STATUS_ALL_RX_TO | SYS_STATUS_ALL_RX_ERR)));
    if (status_reg & SYS_STATUS_RXFCG_BIT_MASK) {
        // Clear interrupt
        dwt_write32bitreg(SYS_STATUS_ID, SYS_STATUS_RXFCG_BIT_MASK);
        // Receive data
        uint16_t frame_len = dwt_read32bitreg(RX_FINFO_ID) & RXFLEN_MASK;
        if (frame_len <= sizeof(rx_buffer)) {
            dwt_readrxdata(rx_buffer, frame_len, 0);

            // Ensure the repsonse is the same
            if (memcmp(rx_buffer, rx_resp_msg, sizeof(rx_expected_msg)) == 0) {
                // Calculate distance
            }
        }


    } else {
        // Clear interrupts
        dwt_write32bitreg(SYS_STATUS_ID, SYS_STATUS_ALL_RX_TO | SYS_STATUS_ALL_RX_ERR);

        
    }


}