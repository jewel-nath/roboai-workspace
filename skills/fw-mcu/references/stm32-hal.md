# STM32 HAL patterns for a robot board

Part of [fw-mcu](../SKILL.md). Names checked on 2026-11-27 against STMicroelectronics'
`stm32f4xx-hal-driver` v1.8.6, with family differences from the G0, G4 and H7 HAL drivers. The
examples are for the F4 family and assume 84 MHz timer clocks (`TIM_CLK_HZ`, take yours from
CubeMX's clock tree); not run. Let STM32CubeMX generate init code and pin
muxing (its licence is ST's SLA0048; the generated HAL is BSD-3-Clause), and keep your own code in
the `USER CODE` blocks or in separate files so regeneration keeps it.

## Clocks

Generate `SystemClock_Config()` in CubeMX's clock tree; do not hand-edit PLL numbers. Then check
what the chip really runs at, once at boot:

```c
printf("sysclk=%lu hclk=%lu pclk1=%lu pclk2=%lu\n",
       HAL_RCC_GetSysClockFreq(), HAL_RCC_GetHCLKFreq(),
       HAL_RCC_GetPCLK1Freq(), HAL_RCC_GetPCLK2Freq());
```

- **Nucleo-64 boards** have no HSE crystal fitted by default; the ST-LINK feeds 8 MHz on its MCO
  pin (board user manual UM1724), so HSE needs `RCC_HSE_BYPASS`, not `RCC_HSE_ON`.
- **Timer clocks** on F4: when an APB prescaler is 1 its timers run at PCLK, otherwise at 2 x PCLK.
  Compute prescaler and period from the timer clock in CubeMX's tree, not from PCLK.
- HSE failing to start sends you to `Error_Handler()`, which spins forever: make it switch the
  outputs off first ([debug.md](debug.md)).

## GPIO and external interrupts

```c
// board.c: an encoder index or limit switch on PA0, rising edge
GPIO_InitTypeDef g = {0};
__HAL_RCC_GPIOA_CLK_ENABLE();
g.Pin = GPIO_PIN_0;
g.Mode = GPIO_MODE_IT_RISING;
g.Pull = GPIO_PULLDOWN;
HAL_GPIO_Init(GPIOA, &g);
HAL_NVIC_SetPriority(EXTI0_IRQn, 5, 0);   // lower number = more urgent; keep the control tick above
HAL_NVIC_EnableIRQ(EXTI0_IRQn);

void EXTI0_IRQHandler(void) { HAL_GPIO_EXTI_IRQHandler(GPIO_PIN_0); }

volatile uint32_t g_limit_hits;
void HAL_GPIO_EXTI_Callback(uint16_t pin)          // F4/F7/H7/G4/L4
{
    if (pin == GPIO_PIN_0) { g_limit_hits++; }     // latch only; the loop acts on it
}
```

G0, C0, U5, H5 and L5 HALs call `HAL_GPIO_EXTI_Rising_Callback()` and
`HAL_GPIO_EXTI_Falling_Callback()` instead. Mechanical switches bounce: count them in the loop
with a time filter, or wire an RC filter, rather than acting on each edge.

## PWM output

```c
// TIM3 CH1 at 20 kHz (example; check the motor driver's PWM range)
#define TIM_CLK_HZ 84000000u                                // timer clock from CubeMX's tree
TIM_HandleTypeDef htim3;

void pwm_init(void)
{
    htim3.Instance = TIM3;
    htim3.Init.Prescaler = 0;
    htim3.Init.CounterMode = TIM_COUNTERMODE_UP;
    htim3.Init.Period = TIM_CLK_HZ / 20000u - 1u;           // ARR = 4199
    htim3.Init.ClockDivision = TIM_CLOCKDIVISION_DIV1;
    htim3.Init.AutoReloadPreload = TIM_AUTORELOAD_PRELOAD_ENABLE;
    HAL_TIM_PWM_Init(&htim3);                               // MspInit enables the TIM clock

    TIM_OC_InitTypeDef oc = {0};
    oc.OCMode = TIM_OCMODE_PWM1;
    oc.Pulse = 0;                                           // start at zero duty
    oc.OCPolarity = TIM_OCPOLARITY_HIGH;
    oc.OCFastMode = TIM_OCFAST_DISABLE;
    HAL_TIM_PWM_ConfigChannel(&htim3, &oc, TIM_CHANNEL_1);
    // CubeMX puts the pin's alternate function in HAL_TIM_MspPostInit(), which it generates
    HAL_TIM_PWM_Start(&htim3, TIM_CHANNEL_1);
}

void pwm_set(float duty)                                    // 0.0 .. 1.0, clamped
{
    if (!(duty > 0.0f)) duty = 0.0f;                        // also catches NaN
    if (duty > 1.0f) duty = 1.0f;
    uint32_t arr = __HAL_TIM_GET_AUTORELOAD(&htim3);
    __HAL_TIM_SET_COMPARE(&htim3, TIM_CHANNEL_1, (uint32_t)(duty * (float)(arr + 1u)));
}
```

Half-bridges driven from advanced timers (TIM1, TIM8) with complementary outputs need dead time
and the break input; that belongs to motor control (`fw-motor-control`, a later batch).

## Control tick

A basic timer (TIM6 or TIM7) interrupt sets the loop rate:

```c
// TIM6 at 1 kHz (example rate): 1 MHz counter, period 1000
htim6.Instance = TIM6;
htim6.Init.Prescaler = TIM_CLK_HZ / 1000000u - 1u;
htim6.Init.Period = 1000u - 1u;
HAL_TIM_Base_Init(&htim6);
HAL_TIM_Base_Start_IT(&htim6);

volatile uint32_t g_tick_due, g_tick_overruns;
void HAL_TIM_PeriodElapsedCallback(TIM_HandleTypeDef *htim)
{
    if (htim->Instance == TIM6) {
        if (g_tick_due) g_tick_overruns++;                  // the loop missed a tick
        g_tick_due = 1;
    }
    // CubeMX also routes the HAL time base here when it uses a timer instead of SysTick
}
```

## ADC scan with circular DMA

```c
#define ADC_CH 2
static volatile uint16_t adc_buf[2 * ADC_CH];               // two halves of a double buffer

void adc_init(void)                                         // DMA2 stream 0, channel 0 (CubeMX sets it up)
{
    hadc1.Instance = ADC1;
    hadc1.Init.ClockPrescaler = ADC_CLOCK_SYNC_PCLK_DIV4;
    hadc1.Init.Resolution = ADC_RESOLUTION_12B;
    hadc1.Init.ScanConvMode = ENABLE;
    hadc1.Init.ContinuousConvMode = ENABLE;
    hadc1.Init.DataAlign = ADC_DATAALIGN_RIGHT;
    hadc1.Init.NbrOfConversion = ADC_CH;                    // the old file left this out
    hadc1.Init.ExternalTrigConv = ADC_SOFTWARE_START;
    hadc1.Init.ExternalTrigConvEdge = ADC_EXTERNALTRIGCONVEDGE_NONE;
    hadc1.Init.DMAContinuousRequests = ENABLE;
    hadc1.Init.EOCSelection = ADC_EOC_SEQ_CONV;
    HAL_ADC_Init(&hadc1);

    ADC_ChannelConfTypeDef ch = {0};
    ch.SamplingTime = ADC_SAMPLETIME_84CYCLES;              // longer for high-impedance sources
    ch.Channel = ADC_CHANNEL_0; ch.Rank = 1; HAL_ADC_ConfigChannel(&hadc1, &ch);
    ch.Channel = ADC_CHANNEL_1; ch.Rank = 2; HAL_ADC_ConfigChannel(&hadc1, &ch);
    HAL_ADC_Start_DMA(&hadc1, (uint32_t *)adc_buf, 2 * ADC_CH);
}

void HAL_ADC_ConvHalfCpltCallback(ADC_HandleTypeDef *h) { adc_take(&adc_buf[0]); }      // first half
void HAL_ADC_ConvCpltCallback(ADC_HandleTypeDef *h)     { adc_take(&adc_buf[ADC_CH]); } // second half
```

`adc_take()` copies the half that DMA just finished; the other half is being written meanwhile.
Free-running continuous conversion samples far faster than a control loop needs; for motor
current, trigger the ADC from the PWM timer instead (`fw-motor-control`).

## UART receive with DMA and idle line

`HAL_UARTEx_ReceiveToIdle_DMA()` replaces the old hand-written IDLE-flag handler. In circular DMA
mode `HAL_UARTEx_RxEventCallback()` runs at half transfer, transfer complete and line idle, and
`Size` is the position in the buffer where the data ends:

```c
#define RX_LEN 256
static uint8_t rx_dma[RX_LEN];
static uint16_t rx_old;

void link_rx_start(void)                                    // DMA stream set to DMA_CIRCULAR in CubeMX
{
    HAL_UARTEx_ReceiveToIdle_DMA(&huart2, rx_dma, RX_LEN);
}

void HAL_UARTEx_RxEventCallback(UART_HandleTypeDef *hu, uint16_t pos)
{
    if (hu != &huart2) return;
    if (pos != rx_old) {
        if (pos > rx_old) {
            ring_push(&rx_dma[rx_old], pos - rx_old);
        } else {                                            // wrapped
            ring_push(&rx_dma[rx_old], RX_LEN - rx_old);
            ring_push(&rx_dma[0], pos);
        }
    }
    rx_old = (pos == RX_LEN) ? 0 : pos;
}

void HAL_UART_ErrorCallback(UART_HandleTypeDef *hu)        // overrun or noise stops reception
{
    if (hu == &huart2) { rx_old = 0; link_rx_start(); }
}
```

`ring_push()` copies into the single-producer ring the main loop parses; frame decoding and
checksums are in [fw-serial-can](../../fw-serial-can/SKILL.md). The DMA and UART IRQ handlers must
call `HAL_DMA_IRQHandler()` and `HAL_UART_IRQHandler()` (CubeMX generates both).

## Independent watchdog

```c
IWDG_HandleTypeDef hiwdg;

void iwdg_init(void)
{
    __HAL_DBGMCU_FREEZE_IWDG();               // stop counting while the debugger halts the core
    hiwdg.Instance = IWDG;
    hiwdg.Init.Prescaler = IWDG_PRESCALER_64; // LSI ~32 kHz typical on F4 (HAL's LSI_VALUE) -> 500 Hz
    hiwdg.Init.Reload = 100;                  // ~200 ms (example); LSI varies a lot, keep margin
#ifdef IWDG_WINDOW_DISABLE
    hiwdg.Init.Window = IWDG_WINDOW_DISABLE;  // G4, L4, F7, H7 and others: 0 would reset on refresh
#endif
    HAL_IWDG_Init(&hiwdg);                    // starts it; it cannot be stopped until reset
}
```

Refresh with `HAL_IWDG_Refresh(&hiwdg)` from the main loop only, as in
[command-watchdog.md](command-watchdog.md). The old file's comment assumed a 40 kHz LSI, which is
the F1's; the F4's typical value is 32 kHz, and the datasheet gives a wide minimum to maximum
range, so test the real timeout on the board.

## Family differences

| Topic | F4 (this file) | Others |
|---|---|---|
| DMA request | `Init.Channel` on a stream (`DMA_CHANNEL_4`) | G0, G4, L4+, H7: DMAMUX, `Init.Request`; H5, U5: GPDMA with its own init |
| EXTI callback | `HAL_GPIO_EXTI_Callback` | G0, C0, U5, H5, L5: Rising and Falling callbacks |
| IWDG | Prescaler, Reload | Window register as well on G4, L4, F7, H7 and others |
| Caches | None | F7, H7: D-cache; DMA buffers in a non-cacheable MPU region, or `SCB_CleanDCache_by_Addr` before TX and `SCB_InvalidateDCache_by_Addr` after RX (32-byte aligned) |
| DMA reach | All SRAM | H7: DMA1/2 cannot reach DTCM (0x2000_0000); place buffers in AXI SRAM or SRAM1-3 |
| Timer clock | 2 x PCLK when the APB prescaler is not 1 | Same idea; H7 and others add more prescaler options; read CubeMX's tree |

Bootloaders: STM32 parts have a ROM bootloader (system memory, entered with BOOT0; ST's AN2606
lists the interfaces per part). Use it, or MCUboot for field updates, rather than a hand-written
jump to the application.
