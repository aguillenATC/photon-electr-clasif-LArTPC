library(ggplot2)
library(reshape2)

time_df = read.csv("time.csv")
time_std_df = read.csv("time_std.csv")
melt_time_df = melt(time_df, id.vars = "X")
melt_time_std_df = melt(time_std_df, id.vars = "X")
# 4 9 2 3 5 1 7 8 6
palette = c("#DFE125","#75A717","#96D223","#0A7411","#BEC01F","#E27425","#E2C225","#E2A325","#1EB227")

ggplot(melt_time_df, aes(x = X)) +
  geom_ribbon(data = melt_time_std_df, aes(ymin = melt_time_df$value - value, 
                                               ymax = melt_time_df$value + value, fill = variable), alpha = .3, show.legend = F) +
  geom_line(aes(y = value, color = variable), size = 2) +
  guides(color = guide_legend(title = "Classifier")) +
  labs(x = "Hit cap", y = "Training time") +
  scale_color_manual(values = palette, labels = c("AdaBoost","Bagging", "CNN", "Gradient Boosting",
                                                  "Linear SVM","LogReg","MLP","Random Forest","XGBoost")) +
  scale_fill_manual(values = palette, labels = c("AdaBoost","Bagging", "CNN", "Gradient Boosting",
                                                  "Linear SVM","LogReg","MLP","Random Forest","XGBoost"))
