from dash import Dash, html, dcc, Input, Output, dash_table
import pandas as pd
import plotly.graph_objects as go
import numpy as np


# ------------------------------------------------------------------------------
# BRAND COLORS  (Clavert Consulting — Brand Option 1)
# ------------------------------------------------------------------------------

NAVY       = "#142941"   # primary dark navy — headers, text, chart lines
STEEL      = "#5D7692"   # secondary — sidebar background
LIGHT_BLUE = "#98C3F4"   # accent — KPI borders, highlights
WARM_GRAY  = "#CBC9C6"   # dividers, subtle separators
OFF_WHITE  = "#F7F5F3"   # page background
WHITE      = "#FFFFFF"

FORECAST_COLOR = "#5D7692"

FONT = "'HK Grotesk', 'Inter', sans-serif"


# ------------------------------------------------------------------------------
# 1)  DATA
# ------------------------------------------------------------------------------

MONTHS = ["Jan","Feb","Mar","Apr","May","Jun",
          "Jul","Aug","Sep","Oct","Nov","Dec"]

MONTHS_NEXT = [f"{m} '25" for m in MONTHS]

raw = {
    "month":     MONTHS,
    "Product A": [100,120,130,115,140,150,145,160,170,155,180,200],
    "Product B": [ 80, 90, 95,100,110,130,125,135,140,130,145,160],
    "Product C": [ 60, 70, 75, 85, 95,105,110,120,115,125,130,145],
}
df = pd.DataFrame(raw)
df_long = df.melt(id_vars="month", var_name="product", value_name="sales")
df_long["month"] = pd.Categorical(df_long["month"], categories=MONTHS, ordered=True)


# ------------------------------------------------------------------------------
# 2)  REUSABLE COMPONENTS
# ------------------------------------------------------------------------------

def kpi_card(label, value_id, sub_label=""):
    return html.Div(
        style={
            "backgroundColor": WHITE,
            "borderRadius": "6px",
            "padding": "18px 22px",
            "flex": "1",
            "borderLeft": f"4px solid {LIGHT_BLUE}",
            "boxShadow": "0 1px 6px rgba(20,41,65,0.08)",
        },
        children=[
            html.P(
                label,
                style={"margin": "0 0 4px 0", "color": STEEL, "fontSize": "10px",
                       "fontWeight": "700", "textTransform": "uppercase", "letterSpacing": "1px"},
            ),
            html.H2(
                id=value_id,
                style={"margin": "0", "color": NAVY, "fontSize": "26px", "fontWeight": "700"},
            ),
            html.P(
                sub_label,
                style={"margin": "3px 0 0 0", "color": WARM_GRAY, "fontSize": "11px"},
            ),
        ],
    )


def sidebar(controls):
    return html.Div(
        style={
            "width": "240px",
            "backgroundColor": NAVY,
            "padding": "28px 18px",
            "flexShrink": "0",
            "display": "flex",
            "flexDirection": "column",
        },
        children=controls + [
            html.Hr(style={"borderColor": "rgba(255,255,255,0.08)", "margin": "28px 0"}),
            html.P("ABOUT", style={"color": LIGHT_BLUE, "fontSize": "10px", "fontWeight": "700",
                                   "letterSpacing": "1.8px", "margin": "0 0 10px 0"}),
            html.P(
                "We help companies turn data into decisions that actually move the business.",
                style={"color": "rgba(255,255,255,0.4)", "fontSize": "12px",
                       "lineHeight": "1.7", "margin": "0"},
            ),
            html.Div(style={"flex": "1"}),
            html.Hr(style={"borderColor": "rgba(255,255,255,0.08)", "margin": "20px 0 16px"}),
            html.P("Simon Herbert",
                   style={"color": WHITE, "fontSize": "12px", "fontWeight": "600", "margin": "0 0 2px 0"}),
            html.P("DATA ANALYST CONSULTANT",
                   style={"color": LIGHT_BLUE, "fontSize": "9px", "fontWeight": "700",
                          "letterSpacing": "1px", "margin": "0 0 4px 0"}),
            html.P("Tel. (34) 607 282 659",
                   style={"color": "rgba(255,255,255,0.3)", "fontSize": "11px", "margin": "0 0 2px 0"}),
            html.P("contact@clavert.com",
                   style={"color": "rgba(255,255,255,0.25)", "fontSize": "11px", "margin": "0"}),
        ],
    )


CHART_LAYOUT = dict(
    paper_bgcolor=WHITE,
    plot_bgcolor=WHITE,
    font=dict(family=FONT, color="#444", size=12),
    margin=dict(l=10, r=10, t=48, b=10),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    xaxis=dict(showgrid=False, zeroline=False),
    yaxis=dict(gridcolor="#f0f0f0", zeroline=False),
)

TAB_STYLE = {
    "backgroundColor": NAVY,
    "color": "rgba(255,255,255,0.45)",
    "border": "none",
    "padding": "14px 32px",
    "fontFamily": FONT,
    "fontSize": "13px",
    "fontWeight": "500",
    "letterSpacing": "0.3px",
}
TAB_SELECTED = {
    **TAB_STYLE,
    "backgroundColor": NAVY,
    "color": WHITE,
    "borderBottom": f"3px solid {LIGHT_BLUE}",
    "fontWeight": "600",
}


# ------------------------------------------------------------------------------
# 3)  APP INIT
# ------------------------------------------------------------------------------

app = Dash(
    __name__,
    external_stylesheets=[
        # HK Grotesk via Fontshare (brand primary font)
        "https://api.fontshare.com/v2/css?f[]=hk-grotesk@400,500,600,700&display=swap",
        # Inter as fallback
        "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap",
    ],
)
app.title = "Clavert | Business Intelligence Dashboard"


# ------------------------------------------------------------------------------
# 4)  LAYOUT
# ------------------------------------------------------------------------------

app.layout = html.Div(
    style={"fontFamily": FONT, "backgroundColor": OFF_WHITE, "minHeight": "100vh"},
    children=[

        # ── HEADER ────────────────────────────────────────────────────────────
        html.Div(
            style={
                "backgroundColor": WHITE,
                "padding": "0 32px",
                "display": "flex",
                "alignItems": "center",
                "justifyContent": "space-between",
                "height": "68px",
                "borderBottom": f"1px solid {WARM_GRAY}",
                "boxShadow": "0 1px 6px rgba(20,41,65,0.07)",
            },
            children=[
                # Logo (Brand Option 1 — dark navy on white)
                html.Img(
                    src="/assets/logo.png",
                    style={"height": "36px", "display": "block"},
                ),
                html.Span(
                    "Business Intelligence Dashboard",
                    style={"color": STEEL, "fontSize": "14px", "fontWeight": "500",
                           "letterSpacing": "0.2px"},
                ),
                # Digital sign
                html.Div(
                    style={"display": "flex", "flexDirection": "column",
                           "alignItems": "flex-end", "lineHeight": "1.3"},
                    children=[
                        html.Span("Simon Herbert",
                                  style={"color": NAVY, "fontWeight": "600", "fontSize": "13px"}),
                        html.Span("DATA ANALYST CONSULTANT",
                                  style={"color": LIGHT_BLUE, "fontSize": "9px",
                                         "fontWeight": "700", "letterSpacing": "1.2px"}),
                        html.Span("Tel. (34) 607 282 659",
                                  style={"color": WARM_GRAY, "fontSize": "10px"}),
                    ],
                ),
            ],
        ),

        # ── TABS ──────────────────────────────────────────────────────────────
        dcc.Tabs(
            id="main-tabs",
            value="tab-simulator",
            style={"borderBottom": "none"},
            colors={"border": NAVY, "primary": LIGHT_BLUE, "background": NAVY},
            children=[

                # ════════════════════════════════════════════════════════════
                #  TAB 1 — SALES TARGET SIMULATOR
                # ════════════════════════════════════════════════════════════
                dcc.Tab(
                    label="  Sales Target Simulator  ",
                    value="tab-simulator",
                    style=TAB_STYLE,
                    selected_style=TAB_SELECTED,
                    children=[
                        html.Div(
                            style={"display": "flex", "minHeight": "calc(100vh - 112px)"},
                            children=[

                                sidebar([
                                    html.P("FILTERS", style={"color": LIGHT_BLUE, "fontSize": "10px",
                                                             "fontWeight": "700", "letterSpacing": "1.8px",
                                                             "margin": "0 0 16px 0"}),
                                    html.Label("Product", style={"color": OFF_WHITE, "fontSize": "12px",
                                                                 "fontWeight": "500", "display": "block",
                                                                 "marginBottom": "6px"}),
                                    dcc.Dropdown(
                                        id="sim-product",
                                        options=[{"label": p, "value": p} for p in df_long["product"].unique()],
                                        value="Product A",
                                        clearable=False,
                                        style={"marginBottom": "26px", "fontSize": "13px"},
                                    ),
                                    html.Label("Target Multiplier", style={"color": OFF_WHITE, "fontSize": "12px",
                                                                           "fontWeight": "500", "display": "block",
                                                                           "marginBottom": "14px"}),
                                    dcc.Slider(
                                        id="sim-multiplier",
                                        min=0.8, max=1.5, step=0.05, value=1.0,
                                        marks={
                                            0.8: {"label": "0.8×", "style": {"color": WARM_GRAY, "fontSize": "11px"}},
                                            1.0: {"label": "1.0×", "style": {"color": WHITE,     "fontSize": "11px"}},
                                            1.2: {"label": "1.2×", "style": {"color": WARM_GRAY, "fontSize": "11px"}},
                                            1.5: {"label": "1.5×", "style": {"color": WARM_GRAY, "fontSize": "11px"}},
                                        },
                                        tooltip={"placement": "bottom", "always_visible": True},
                                    ),
                                ]),

                                html.Div(
                                    style={"flex": "1", "padding": "28px 30px", "overflowY": "auto"},
                                    children=[

                                        html.Div(
                                            style={"display": "flex", "gap": "14px", "marginBottom": "22px"},
                                            children=[
                                                kpi_card("Total Actual Sales", "sim-kpi-actual", "units — full year"),
                                                kpi_card("Total Target Sales", "sim-kpi-target", "units — full year"),
                                                kpi_card("Avg Monthly Actual", "sim-kpi-avg",    "units / month"),
                                                kpi_card("Gap to Target",      "sim-kpi-gap",    "units · actual vs target"),
                                            ],
                                        ),

                                        html.Div(
                                            style={"display": "flex", "gap": "14px", "marginBottom": "22px"},
                                            children=[
                                                html.Div(
                                                    style={"flex": "2", "backgroundColor": WHITE,
                                                           "borderRadius": "6px", "padding": "16px",
                                                           "boxShadow": "0 1px 6px rgba(20,41,65,0.08)"},
                                                    children=[dcc.Graph(id="sim-line-chart",
                                                                        config={"displayModeBar": False})],
                                                ),
                                                html.Div(
                                                    style={"flex": "1", "backgroundColor": WHITE,
                                                           "borderRadius": "6px", "padding": "16px",
                                                           "boxShadow": "0 1px 6px rgba(20,41,65,0.08)"},
                                                    children=[dcc.Graph(id="sim-bar-chart",
                                                                        config={"displayModeBar": False})],
                                                ),
                                            ],
                                        ),

                                        html.Div(
                                            style={"backgroundColor": WHITE, "borderRadius": "6px",
                                                   "padding": "20px 22px",
                                                   "boxShadow": "0 1px 6px rgba(20,41,65,0.08)"},
                                            children=[
                                                html.P("Monthly Breakdown",
                                                       style={"fontWeight": "600", "color": NAVY,
                                                              "fontSize": "13px", "margin": "0 0 14px 0"}),
                                                dash_table.DataTable(
                                                    id="sim-table",
                                                    style_header={
                                                        "backgroundColor": NAVY, "color": WHITE,
                                                        "fontWeight": "600", "fontSize": "11px",
                                                        "textTransform": "uppercase", "letterSpacing": "0.6px",
                                                        "border": "none", "padding": "10px 14px",
                                                    },
                                                    style_cell={
                                                        "fontFamily": FONT, "fontSize": "13px",
                                                        "padding": "9px 14px", "border": "none",
                                                        "borderBottom": f"1px solid {OFF_WHITE}", "color": "#333",
                                                    },
                                                    style_data_conditional=[
                                                        {"if": {"row_index": "odd"},
                                                         "backgroundColor": OFF_WHITE},
                                                        {"if": {"filter_query": "{Gap} < 0"},
                                                         "color": "#c0392b", "fontWeight": "600"},
                                                        {"if": {"filter_query": "{Gap} > 0"},
                                                         "color": "#27ae60", "fontWeight": "600"},
                                                    ],
                                                    page_size=12,
                                                    sort_action="native",
                                                ),
                                            ],
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),

                # ════════════════════════════════════════════════════════════
                #  TAB 2 — SALES FORECASTING TOOL
                # ════════════════════════════════════════════════════════════
                dcc.Tab(
                    label="  Sales Forecasting Tool  ",
                    value="tab-forecast",
                    style=TAB_STYLE,
                    selected_style=TAB_SELECTED,
                    children=[
                        html.Div(
                            style={"display": "flex", "minHeight": "calc(100vh - 112px)"},
                            children=[

                                sidebar([
                                    html.P("SETTINGS", style={"color": LIGHT_BLUE, "fontSize": "10px",
                                                              "fontWeight": "700", "letterSpacing": "1.8px",
                                                              "margin": "0 0 16px 0"}),
                                    html.Label("Product", style={"color": OFF_WHITE, "fontSize": "12px",
                                                                 "fontWeight": "500", "display": "block",
                                                                 "marginBottom": "6px"}),
                                    dcc.Dropdown(
                                        id="fc-product",
                                        options=[{"label": p, "value": p} for p in df_long["product"].unique()],
                                        value="Product A",
                                        clearable=False,
                                        style={"marginBottom": "26px", "fontSize": "13px"},
                                    ),
                                    html.Label("Forecast Horizon (months)", style={"color": OFF_WHITE, "fontSize": "12px",
                                                                                   "fontWeight": "500", "display": "block",
                                                                                   "marginBottom": "14px"}),
                                    dcc.Slider(
                                        id="fc-horizon",
                                        min=1, max=6, step=1, value=3,
                                        marks={i: {"label": f"{i}m", "style": {"color": WARM_GRAY, "fontSize": "11px"}}
                                               for i in range(1, 7)},
                                        tooltip={"placement": "bottom", "always_visible": True},
                                    ),
                                    html.Hr(style={"borderColor": "rgba(255,255,255,0.08)", "margin": "24px 0"}),
                                    html.Label("Forecast Method", style={"color": OFF_WHITE, "fontSize": "12px",
                                                                         "fontWeight": "500", "display": "block",
                                                                         "marginBottom": "12px"}),
                                    dcc.RadioItems(
                                        id="fc-method",
                                        options=[
                                            {"label": " Linear Trend",    "value": "linear"},
                                            {"label": " Moving Average",  "value": "ma"},
                                        ],
                                        value="linear",
                                        labelStyle={"display": "block", "color": "rgba(255,255,255,0.8)",
                                                    "fontSize": "13px", "marginBottom": "10px"},
                                        inputStyle={"marginRight": "8px", "accentColor": LIGHT_BLUE},
                                    ),
                                    html.Div(
                                        id="fc-method-desc",
                                        style={"color": "rgba(255,255,255,0.32)", "fontSize": "11px",
                                               "lineHeight": "1.6", "marginTop": "10px"},
                                    ),
                                ]),

                                html.Div(
                                    style={"flex": "1", "padding": "28px 30px", "overflowY": "auto"},
                                    children=[

                                        html.Div(
                                            style={"display": "flex", "gap": "14px", "marginBottom": "22px"},
                                            children=[
                                                kpi_card("Forecasted Total",     "fc-kpi-total",  "units — forecast period"),
                                                kpi_card("Avg Monthly Forecast", "fc-kpi-avg",    "units / month"),
                                                kpi_card("Monthly Growth Rate",  "fc-kpi-growth", "% change per month"),
                                                kpi_card("Forecast Method",      "fc-kpi-method", "algorithm used"),
                                            ],
                                        ),

                                        html.Div(
                                            style={"backgroundColor": WHITE, "borderRadius": "6px",
                                                   "padding": "16px",
                                                   "boxShadow": "0 1px 6px rgba(20,41,65,0.08)",
                                                   "marginBottom": "22px"},
                                            children=[dcc.Graph(id="fc-chart", config={"displayModeBar": False})],
                                        ),

                                        html.Div(
                                            style={"backgroundColor": WHITE, "borderRadius": "6px",
                                                   "padding": "20px 22px",
                                                   "boxShadow": "0 1px 6px rgba(20,41,65,0.08)"},
                                            children=[
                                                html.P("Forecast Details",
                                                       style={"fontWeight": "600", "color": NAVY,
                                                              "fontSize": "13px", "margin": "0 0 14px 0"}),
                                                dash_table.DataTable(
                                                    id="fc-table",
                                                    style_header={
                                                        "backgroundColor": NAVY, "color": WHITE,
                                                        "fontWeight": "600", "fontSize": "11px",
                                                        "textTransform": "uppercase", "letterSpacing": "0.6px",
                                                        "border": "none", "padding": "10px 14px",
                                                    },
                                                    style_cell={
                                                        "fontFamily": FONT, "fontSize": "13px",
                                                        "padding": "9px 14px", "border": "none",
                                                        "borderBottom": f"1px solid {OFF_WHITE}", "color": "#333",
                                                    },
                                                    style_data_conditional=[
                                                        {"if": {"row_index": "odd"},
                                                         "backgroundColor": OFF_WHITE},
                                                        {"if": {"filter_query": '{Type} = "Forecast"'},
                                                         "color": NAVY, "fontWeight": "600"},
                                                    ],
                                                    page_size=18,
                                                    sort_action="native",
                                                ),
                                            ],
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),

            ],
        ),
    ],
)


# ------------------------------------------------------------------------------
# 5)  CALLBACK — TAB 1: Sales Target Simulator
# ------------------------------------------------------------------------------

@app.callback(
    Output("sim-line-chart",  "figure"),
    Output("sim-bar-chart",   "figure"),
    Output("sim-table",       "data"),
    Output("sim-table",       "columns"),
    Output("sim-kpi-actual",  "children"),
    Output("sim-kpi-target",  "children"),
    Output("sim-kpi-avg",     "children"),
    Output("sim-kpi-gap",     "children"),
    Input("sim-product",      "value"),
    Input("sim-multiplier",   "value"),
)
def update_simulator(selected_product, multiplier):
    dff = (
        df_long[df_long["product"] == selected_product]
        .copy()
        .sort_values("month")
    )
    dff["target"] = (dff["sales"] * multiplier).round(1)
    dff["gap"]    = (dff["target"] - dff["sales"]).round(1)

    fig_line = go.Figure()
    fig_line.add_trace(go.Scatter(
        x=dff["month"], y=dff["sales"], name="Actual",
        mode="lines+markers",
        line=dict(color=NAVY, width=2.5),
        marker=dict(size=7, color=NAVY, line=dict(color=WHITE, width=1.5)),
    ))
    fig_line.add_trace(go.Scatter(
        x=dff["month"], y=dff["target"], name="Target",
        mode="lines+markers",
        line=dict(color=LIGHT_BLUE, width=2.5, dash="dash"),
        marker=dict(size=7, color=LIGHT_BLUE, line=dict(color=WHITE, width=1.5)),
    ))
    fig_line.update_layout(
        title=dict(text=f"Actual vs Target — {selected_product}",
                   font=dict(size=13, color=NAVY, family=FONT)),
        **CHART_LAYOUT,
    )

    totals = df_long.groupby("product", observed=True)["sales"].sum().reset_index()
    totals["target_total"] = (totals["sales"] * multiplier).round(1)

    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(name="Actual", x=totals["product"], y=totals["sales"],
                             marker_color=NAVY, marker_line_width=0))
    fig_bar.add_trace(go.Bar(name="Target", x=totals["product"], y=totals["target_total"],
                             marker_color=LIGHT_BLUE, marker_line_width=0))
    fig_bar.update_layout(
        title=dict(text="Annual Total — All Products",
                   font=dict(size=13, color=NAVY, family=FONT)),
        barmode="group",
        **CHART_LAYOUT,
    )

    table_df = dff[["month","sales","target","gap"]].rename(
        columns={"month": "Month", "sales": "Actual", "target": "Target", "gap": "Gap"}
    )

    total_actual = int(dff["sales"].sum())
    total_target = int(dff["target"].sum())
    avg_actual   = f"{dff['sales'].mean():.1f}"
    gap          = total_target - total_actual
    gap_str      = f"+{gap:,}" if gap >= 0 else f"{gap:,}"

    return (
        fig_line,
        fig_bar,
        table_df.to_dict("records"),
        [{"name": c, "id": c} for c in table_df.columns],
        f"{total_actual:,}",
        f"{total_target:,}",
        avg_actual,
        gap_str,
    )


# ------------------------------------------------------------------------------
# 6)  CALLBACK — TAB 2: Sales Forecasting Tool
# ------------------------------------------------------------------------------

@app.callback(
    Output("fc-chart",       "figure"),
    Output("fc-table",       "data"),
    Output("fc-table",       "columns"),
    Output("fc-kpi-total",   "children"),
    Output("fc-kpi-avg",     "children"),
    Output("fc-kpi-growth",  "children"),
    Output("fc-kpi-method",  "children"),
    Output("fc-method-desc", "children"),
    Input("fc-product",      "value"),
    Input("fc-horizon",      "value"),
    Input("fc-method",       "value"),
)
def update_forecast(selected_product, horizon, method):
    dff = (
        df_long[df_long["product"] == selected_product]
        .copy()
        .sort_values("month")
    )
    sales  = dff["sales"].to_numpy(dtype=float)
    n      = len(sales)
    x_hist = np.arange(n)

    if method == "linear":
        coeffs      = np.polyfit(x_hist, sales, 1)
        x_fc        = np.arange(n, n + horizon)
        fc_values   = np.polyval(coeffs, x_fc).round(1)
        method_name = "Linear Trend"
        method_desc = (
            "Fits a straight line through all historical months "
            "using least-squares regression, then extrapolates forward."
        )
    else:
        window       = 3
        last_avg     = sales[-window:].mean()
        recent_slope = (sales[-1] - sales[-window]) / window
        fc_values    = np.array([
            round(last_avg + recent_slope * (i + 1), 1)
            for i in range(horizon)
        ])
        method_name = "Moving Average"
        method_desc = (
            f"Averages the last {window} months and projects forward "
            "using a gentle slope derived from that window."
        )

    fc_labels = MONTHS_NEXT[:horizon]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=list(dff["month"]),
        y=sales.tolist(),
        name="Historical",
        mode="lines+markers",
        line=dict(color=NAVY, width=2.5),
        marker=dict(size=7, color=NAVY, line=dict(color=WHITE, width=1.5)),
    ))

    bridge_x = [MONTHS[-1]] + fc_labels
    bridge_y = [float(sales[-1])] + fc_values.tolist()
    fig.add_trace(go.Scatter(
        x=bridge_x,
        y=bridge_y,
        name="Forecast",
        mode="lines+markers",
        line=dict(color=STEEL, width=2.5, dash="dot"),
        marker=dict(size=8, color=STEEL,
                    symbol="diamond", line=dict(color=WHITE, width=1.5)),
    ))

    upper = (fc_values * 1.10).tolist()
    lower = (fc_values * 0.90).tolist()
    fig.add_trace(go.Scatter(
        x=fc_labels + fc_labels[::-1],
        y=upper + lower[::-1],
        fill="toself",
        fillcolor="rgba(93,118,146,0.10)",
        line=dict(color="rgba(0,0,0,0)"),
        hoverinfo="skip",
        showlegend=True,
        name="±10% band",
    ))

    fig.update_layout(
        title=dict(
            text=f"Sales Forecast — {selected_product}  ({method_name}, {horizon}m horizon)",
            font=dict(size=13, color=NAVY, family=FONT),
        ),
        **CHART_LAYOUT,
    )

    hist_rows = [
        {"Month": m, "Sales": int(s), "Type": "Historical", "vs Prev Month": ""}
        for m, s in zip(dff["month"].astype(str), sales)
    ]
    fc_rows = []
    prev = float(sales[-1])
    for label, val in zip(fc_labels, fc_values):
        change = ((val - prev) / prev * 100) if prev else 0
        fc_rows.append({
            "Month": label,
            "Sales": val,
            "Type": "Forecast",
            "vs Prev Month": f"{change:+.1f}%",
        })
        prev = val

    table_data    = hist_rows + fc_rows
    table_columns = [{"name": c, "id": c} for c in ["Month", "Sales", "Type", "vs Prev Month"]]

    fc_total  = fc_values.sum()
    fc_avg    = fc_values.mean()
    last_sale = float(sales[-1])
    growth    = ((fc_values[0] - last_sale) / last_sale * 100) if last_sale else 0

    return (
        fig,
        table_data,
        table_columns,
        f"{fc_total:,.0f}",
        f"{fc_avg:,.1f}",
        f"{growth:+.1f}%",
        method_name,
        method_desc,
    )


# ------------------------------------------------------------------------------
# 7)  RUN
# ------------------------------------------------------------------------------

server = app.server  # required by gunicorn for production

if __name__ == "__main__":
    app.run_server(debug=True)
