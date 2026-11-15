import pandas as pd


def generate_climate_report(fingerprint, trends, relationships, anomalies):

    report = []

    report.append("EARTHSCOPE AI - CLIMATE INVESTIGATION")
    report.append("=" * 55)

    # Climate fingerprint investigation

    report.append("\n1. CLIMATE FINGERPRINT")

    for variable, values in fingerprint.items():

        report.append(
            f"{variable}: Average = {values['average']}, "
            f"Variability = {values['variability']}"
        )

    # Long-term trend investigation

    report.append("\n2. LONG-TERM TREND INVESTIGATION")

    for variable, information in trends.items():

        report.append(
            f"{variable}: {information['direction']} "
            f"(Monthly slope: {information['monthly_change']})"
        )

        if (
            information["lower_slope"] <= 0
            <= information["upper_slope"]
        ):
            report.append(
                "  Note: The estimated slope interval includes zero; "
                "the trend direction is uncertain."
            )

    # Environmental anomaly investigation

    report.append("\n3. ANOMALY INVESTIGATION")

    for column in anomalies.columns:

        if column.endswith("_Anomaly"):

            count = int(anomalies[column].sum())

            report.append(
                f"{column.replace('_Anomaly', '')}: "
                f"{count} unusual observations detected."
            )

    # Relationship investigation

    report.append("\n4. ENVIRONMENTAL RELATIONSHIPS")

    if isinstance(relationships, pd.DataFrame):

        columns = relationships.columns

        for i in range(len(columns)):

            for j in range(i + 1, len(columns)):

                first = columns[i]
                second = columns[j]

                correlation = relationships.loc[first, second]

                if pd.isna(correlation):
                    continue

                if abs(correlation) >= 0.7:
                    strength = "Strong"

                elif abs(correlation) >= 0.4:
                    strength = "Moderate"

                else:
                    strength = "Weak"

                direction = (
                    "positive" if correlation > 0
                    else "negative"
                )

                report.append(
                    f"{first} and {second}: "
                    f"{strength} {direction} association "
                    f"({correlation:.2f})"
                )

    # Scientific caution

    report.append("\n5. SCIENTIFIC INTERPRETATION")

    report.append(
        "Detected associations do not establish causation. "
        "Unusual observations are not automatically evidence "
        "of long-term climate change."
    )

    report.append(
        "Further investigation using additional locations, "
        "longer time periods and independent datasets is recommended."
    )

    return "\n".join(report)


def save_climate_report(report):

    with open(
        "data/processed/climate_investigation_report.txt",
        "w",
        encoding="utf-8"
    ) as file:

        file.write(report)

    print("Climate investigation report saved successfully.")
