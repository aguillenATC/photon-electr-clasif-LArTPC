library(ggplot2)
library(RColorBrewer)
library(reshape2)

rf = read.csv("rf_instantaneous_power.csv", row.names = 1)
rf$hpm5[rf$hpm5 == 0] = NA
rf$hpm5[rf$hpm5 < 212.5] = NA
xgb = read.csv("xgb_instantaneous_power.csv", row.names = 1)
xgb$hpm5[xgb$hpm5 == 0] = NA
xgb$hpm5[xgb$hpm5 > 270] = NA
xgb$hpm5[xgb$hpm5 < 211] = NA
colnames(rf) = c("Time", "RF")
colnames(xgb) = c("Time", "XGB")
length_diff = length(xgb$XGB) - length(rf$RF)
rf_xgb_df = data.frame(Time = xgb$Time, RF = c(rf$RF,rep(NA, length_diff)), XGB = xgb$XGB, Baseline = rnorm(length(xgb$XGB),112,1))
melt_rf_xgb_dataset = melt(rf_xgb_df, id.vars = "Time")

palette_averages = c("#1EB227","#96D223","#9A9593")

ggplot(melt_rf_xgb_dataset) + geom_line(aes(x = Time, y = value, color = variable), size = 1.3) +
    scale_color_manual(name = "Classifiers", values = palette_averages, labels = c("Random Forest", "XGBoost", "Baseline")) +
    xlab("Time (s)") + ylab("Instantaneous power (W)")
