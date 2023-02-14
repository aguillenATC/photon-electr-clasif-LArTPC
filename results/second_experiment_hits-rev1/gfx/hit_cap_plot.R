library(ggplot2)
library(reshape2)

accuracy_df = read.csv("accuracy.csv")
accuracy_std_df = read.csv("accuracy_std.csv")
max_accuracy_df = data.frame(pos = accuracy_df$X[apply(accuracy_df[,-1],2,which.max)], value = apply(accuracy_df[,-1],2,max))
accuracy_df["cnn"][accuracy_df["cnn"] == 0] = NA
melt_accuracy_df = melt(accuracy_df, id.vars = "X")
melt_accuracy_std_df = melt(accuracy_std_df, id.vars = "X")
palette = c("#BEC01F","#75A717","#DFE125","#96D223","#E27425","#E2A325","#E2C225","#0A7411","#1EB227")

ggplot(melt_accuracy_df, aes(x = X)) +
  geom_ribbon(data = melt_accuracy_std_df, aes(ymin = melt_accuracy_df$value - value, 
                                               ymax = melt_accuracy_df$value + value, fill = variable), alpha = .3, show.legend = F) +
  geom_line(aes(y=value,color=variable), size = 2) +
  geom_point(data = max_accuracy_df, aes(y = value, x = pos), size = 3) +
  geom_text(data = max_accuracy_df, aes(y = value, x = pos, label = pos), hjust=0.5, vjust=1.6) +
  guides(color = guide_legend(title = "Classifier")) +
  labs(x = "Hit cap", y = "Classification accuracy (validation)") +
  scale_color_manual(values = palette, labels = c("AdaBoost","Bagging", "CNN", "Gradient Boosting",
                                                  "Linear SVM","LogReg","MLP","Random Forest","XGBoost")) +
  scale_fill_manual(values = palette, labels = c("AdaBoost","Bagging", "CNN", "Gradient Boosting",
                                                  "Linear SVM","LogReg","MLP","Random Forest","XGBoost"))
