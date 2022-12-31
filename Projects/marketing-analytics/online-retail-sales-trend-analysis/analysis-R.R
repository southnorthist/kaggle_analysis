library(tidyverse)
library(lubridate)
library(patchwork)
#library(hrbrthemes)

# Set the working directory
dir_path <- "/Users/qianyihuang/Documents/Qianyi_Folder/DS_Project/GitHub/Data_Science_Playground/Projects/marketing-analytics/online-retail-sales-trend-analysis"
setwd(dir_path)
# Read in the data set
retail_sale <- read_csv('inu_neko_orderline_clean.csv')
# Quick look at the data
head(retail_sale)
# number of rows and columns
glimpse(retail_sale)
# How many years does the order data cover?
unique(retail_sale$trans_year)
# How many months does the online order data cover?
unique(retail_sale$trans_month)
retail_sale %>%
  group_by(trans_month) %>%
  summarise(n = n())

# Cross-check date 
## Check month - okay
table(month(retail_sale$trans_timestamp), retail_sale$trans_month)
## Check day
table(day(retail_sale$trans_timestamp), retail_sale$trans_day)
## Check hour - same as trans_day - need to be corrected
table(hour(retail_sale$trans_timestamp), retail_sale$trans_hour)
table(retail_sale$trans_day, retail_sale$trans_hour)
## Create date
retail_sale$trans_date <- date(retail_sale$trans_timestamp)
## Correct trans_hour variable
retail_sale$trans_hour <- hour(retail_sale$trans_timestamp)

# Sales Trend
grouped_day <- retail_sale %>% 
  group_by(trans_date) %>%
  summarise(unique_cust_per_day = n_distinct(cust_id), 
            total_sales_per_day = sum(total_sales), 
            total_quantity_per_day = sum(trans_quantity))

grouped_cust_day <- retail_sale %>%
  group_by(trans_date, cust_id) %>%
  summarise(total_sales_per_cust_day = sum(total_sales)) %>%
  ungroup() %>%
  group_by(trans_date) %>%
  summarise(mean_daily_sales = mean(total_sales_per_cust_day),
            sd_daily_sales = sd(total_sales_per_cust_day),
            n_daily_cust = n_distinct(cust_id)) %>%
  mutate(se_daily_sales = sd_daily_sales /sqrt(n_daily_cust) * qt(0.975, n_daily_cust)) %>%
  fill(se_daily_sales, .direction = 'down') %>%
  rowwise() %>%
  mutate(low = max(0, mean_daily_sales - se_daily_sales),
         high = mean_daily_sales + se_daily_sales)
 
# Daily Total Sales/Quantity
coef <- 20
p1 <- ggplot(data = grouped_day, aes(x = trans_date)) + 
  geom_line(aes(y = total_sales_per_day), color = '#1e81b0', linewidth = 1) + 
  geom_bar(aes(y = total_quantity_per_day * coef), stat = 'identity', 
           linewidth = .1, color = 'seagreen', alpha = 0.3) + 
  scale_y_continuous(
    # Features of the first axis
    name = "Total Sales Per Day",
    
    # Add a second axis and specify its features
    sec.axis = sec_axis(~.* 1/coef, name = "Total Quantity Per Day")
  ) + 
  ggtitle('Daily Total Sales/Quantity') +
  labs(x = "Transaction Date") +
  theme_bw() +
  theme(
    axis.title.y = element_text(color = '#1e81b0', size=10),
    axis.title.y.right = element_text(color = 'seagreen', size=10)
  ) 

# Average Daily Sales Per Customer with 95% CI
p2 <- ggplot(data = grouped_cust_day, aes(x = trans_date, y = mean_daily_sales)) + 
  geom_line(color = '#1e81b0', linewidth = 1) + 
  geom_ribbon(aes(ymin =  low, ymax = high), fill = '#adcae6', alpha = 0.6) + 
  ggtitle('Average Daily Sales Per Customer with 95% CI') + 
  labs(x = 'Transaction Date', y = 'Average Daily Sales' ) + 
  theme_bw()
p3 <- ggplot(data = grouped_cust_day, aes(x = trans_date, y = n_daily_cust)) + 
  geom_line(color = '#1e81b0',linewidth = 1) + 
  ggtitle(('Daily Number of Unique Customers')) + 
  labs(x = 'Transaction Date', y = 'Count') + 
  theme_bw()
p1 + p2 + p3



# Customer Demographics
unique_cust_age_df <- retail_sale %>%
  distinct(cust_id, trans_month, cust_age, .keep_all = FALSE)
# median of the age by month
unique_cust_age_df %>%
  group_by(trans_month) %>%
  summarise(median_age = median(cust_age))
## Customer age distribution using boxplot across transaction months
ggplot(data = unique_cust_age_df, aes(y = cust_age)) + 
  geom_boxplot(fill = '#1e81b0') + 
  facet_wrap(~ trans_month, nrow = 1) + 
  theme_bw() + 
  ggtitle('Unique Customer Age Distribution over Months') +
  labs(x = NULL, y = "Customer Age") +
  theme(
    axis.text.x = element_blank(),
    axis.ticks.x = element_blank()
  )


## Correlation between age and total sales
sales_age_month <- retail_sale %>%
  group_by(cust_id, trans_month, cust_age) %>%
  summarise(month_sales = sum(total_sales),
            month_quantity = sum(trans_quantity))
### Correlation coefficient
sales_age_month %>% ungroup() %>%
  group_by(trans_month) %>%
  summarise(cor_age_sales = cor(cust_age, month_sales),
         cor_age_quantity = cor(cust_age, month_quantity))
### Scatter plots
ggplot(data = sales_age_month, aes(x = cust_age)) + 
  geom_point(aes(y = month_sales), color = '#1e81b0', alpha = 0.1) + 
  facet_wrap(~ trans_month) + 
  ggtitle('Customer Age vs. Monthly Sales') +
  labs(x = 'Customer Age', y = 'Monthly Sales')+
  theme_bw()
## Correlation between age and total quantity
ggplot(data = sales_age_month, aes(x = cust_age)) + 
  geom_point(aes(y = month_quantity), color = '#1e81b0', alpha = 0.1) + 
  facet_wrap(~ trans_month) + 
  ggtitle('Customer Age vs. Monthly Quantity Sold') +
  labs(x = 'Customer Age', y = 'Monthly Quantity Sold')+
  theme_bw()


## Customer State Sales
month_state_sales <- retail_sale %>%
  group_by(trans_month, cust_state) %>%
  summarise(month_state_sales = sum(total_sales),
            month_state_quantity = sum(trans_quantity),
            month_unique_cust = n_distinct(cust_id))
## Bar plot by state and transaction month
bp <-  ggplot(data = month_state_sales)  
### Unique number of customers
bp + geom_bar(aes(x = month_unique_cust, 
                  y = reorder(cust_state, month_unique_cust)), 
              stat = 'identity', fill = '#1e81b0') +
  facet_grid(cols = vars(trans_month)) + 
  ggtitle('Number of Unique Customers by State over 6 Months') + 
  labs(x = 'Number of Customers', y = 'Customer State') +
  theme_classic()
### Total Sales
bp + geom_bar(aes(x = month_state_sales, 
                  y = reorder(cust_state, month_state_sales)), 
              stat = 'identity', fill = '#1e81b0') +
  facet_grid(cols = vars(trans_month)) + 
  ggtitle('Monthly Total Sales by State over 6 Months') + 
  labs(x = 'Total Sales', y = 'Customer State') +
  theme_classic()

## Customer purchasing behavior

### Purchase by state
month_state_purchase <- retail_sale %>%
  group_by(trans_month, cust_state, cust_id) %>%
  summarise(month_total_per_cust = sum(total_sales)) %>% ungroup() %>%
  group_by(trans_month, cust_state) %>%
  summarise(avg_month_sales_per_cust = mean(month_total_per_cust),
            n_month_per_cust = n())
cond <- month_state_purchase %>% ungroup() %>% 
  filter(n_month_per_cust > 30 & trans_month == 6) %>% 
  select(cust_state)

month_state_purchase[month_state_purchase$cust_state %in% cond$cust_state, ] %>%
  ggplot(aes(x = trans_month, y = avg_month_sales_per_cust, 
             color = cust_state)) +
  geom_line(linewidth = 0.5) + 
  ggtitle('Average Monthly Sales Per Customer by States') + 
  scale_x_continuous(name = 'Transaction Month', breaks = seq(1, 7, 1)) +
  scale_y_continuous(name = 'Average Monthly Sales', breaks = seq(0, 160, 20)) +
  theme_classic()

### Purchase by product type

plot_by_ma <- function(cond){
  if(cond == 'All States'){
    df <- retail_sale %>%
      group_by(trans_month, prod_animal_type) %>%
      summarise(month_sales_per_prod = sum(total_sales),
                month_quantity_per_prod = sum(trans_quantity)) %>% ungroup()
  } else{
    df <- retail_sale %>% filter(cust_state == cond) %>%
      group_by(trans_month, prod_animal_type) %>%
      summarise(month_sales_per_prod = sum(total_sales),
                month_quantity_per_prod = sum(trans_quantity)) %>% ungroup()
  }
  p1 <- ggplot(data = df, 
               aes(x = factor(trans_month), group = prod_animal_type,
                   color = prod_animal_type)) + 
    geom_line(aes(y = month_sales_per_prod)) + 
    geom_point(aes(y = month_sales_per_prod)) +
    theme_classic() +
    labs(x = 'Transaction Month', y = 'Monthly Sales') +
    theme(legend.position = 'bottom')
  
  p2 <- ggplot(data = df, 
               aes(x = factor(trans_month), group = prod_animal_type,
                   fill = prod_animal_type, color = prod_animal_type)) + 
    geom_bar(aes(y = month_quantity_per_prod), stat = 'identity', position = 'dodge') + 
    theme_classic() + 
    labs(x = 'Transaction Month', y = 'Monthly Quantity Sold') +
    theme(legend.position = 'bottom')
  p1 + p2 + plot_annotation(title = paste('Monthly Sales and Quantity by Product Animal Type', cond, sep = ' - '))
  
}

plot_by_ma('All States')
plot_by_ma('New York')
plot_by_ma('New Jersey')
plot_by_ma('Pennsylvania')


### Purchase by Product category and Animal Type
plot_by_mac <- function(cond){
  if(cond == 'All States'){
    df <- retail_sale %>%
      group_by(trans_month, prod_animal_type, prod_category) %>%
      summarise(month_sales_per_prod = sum(total_sales),
                month_quantity_per_prod = sum(trans_quantity)) %>% ungroup()
  } else{
    df <- retail_sale %>% filter(cust_state == cond) %>%
      group_by(trans_month, prod_animal_type, prod_category) %>%
      summarise(month_sales_per_prod = sum(total_sales),
                month_quantity_per_prod = sum(trans_quantity)) %>% ungroup()
  }
  
  p1 <- ggplot(data = df,
         aes(x = factor(trans_month), group = prod_category,
             color = prod_category)) + 
    geom_line(aes(y = month_sales_per_prod), linewidth = 1) + 
    geom_point(aes(y = month_sales_per_prod), size = 3) +
    facet_grid(cols = vars(prod_animal_type)) + 
    theme_bw() +
    labs(x = 'Transaction Month', y = 'Monthly Sales') +
    theme(legend.position = 'bottom')+ 
    ggtitle(paste('Total Sales by Month, Product Animal Type and Product Category', cond, sep = ' - '))

  p2 <- ggplot(data = df, 
         aes(x = factor(trans_month), group = prod_category,
             color = prod_category)) + 
    geom_line(aes(y = month_quantity_per_prod), linewidth = 1) + 
    geom_point(aes(y = month_quantity_per_prod), size = 3) +
    facet_grid(cols = vars(prod_animal_type)) + 
    theme_bw() +
    labs(x = 'Transaction Month', y = 'Monthly Quantity Sold') +
    theme(legend.position = 'bottom') + 
    ggtitle(paste('Total Quantity Sold by Month, Product Animal Type and Product Category', cond, sep =' - '))  
  
  p1/p2
}

plot_by_mac('All States')
plot_by_mac('New York')
plot_by_mac('New Jersey')
plot_by_mac('Pennsylvania')

## Cohort Analysis
cohort_pop <- retail_sale %>% 
  group_by(cust_id) %>%
  mutate(cohort_month = first(trans_month),
         cohort_index = trans_month - first(trans_month) + 1) %>%
  group_by(cohort_month, cohort_index) %>%
  summarise(count_cust = n_distinct(cust_id),
            mean_quantity = mean(trans_quantity),
            mean_sales = mean(total_sales)) %>% 
  mutate(acq_count = first(count_cust),
         count_perc = count_cust / acq_count)
# Number of customers
cohort_pop %>%
  pivot_wider(id_cols = cohort_month, 
             names_from = cohort_index,
             names_prefix = 'ch_index_',
             values_from = count_cust)
# Retention Rates
percent <- function(x, digits = 2, format = "f", ...) {
  paste0(formatC(100 * x, format = format, digits = digits, ...), "%")
}

ggplot(data = cohort_pop, aes(x = factor(cohort_index), 
                              y = factor(reorder(cohort_month, cohort_index)), 
                              fill = count_perc)) + 
  geom_tile(color = 'black') + 
  geom_text(aes(label = percent(count_perc, digits=1)), color = "white", size = 4) +
  coord_fixed() + 
  ggtitle('Retention Rates by Cohort Over Time') + 
  labs(x = 'Month since Acquisition', y = 'Month of Acquisition')

# Average quantity sold per transaction
cohort_pop %>%
  pivot_wider(id_cols = cohort_month, 
              names_from = cohort_index,
              names_prefix = 'ch_index_',
              values_from = mean_quantity)
# Average sales per transaction
cohort_pop %>%
  pivot_wider(id_cols = cohort_month, 
              names_from = cohort_index,
              names_prefix = 'ch_index_',
              values_from = mean_sales)
