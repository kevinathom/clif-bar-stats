setwd("/home/kevin/PycharmProjects/ClifBarBar")

# Import data, removing row numbers
clif_data <- read.csv("clif_products.csv")
clif_data <- clif_data[ , 2:ncol(clif_data)]

# Label Minis
clif_data$Brand_1 <- as.character(clif_data$Brand_1)
for(i in 1:nrow(clif_data)){
  if(grepl(".*Minis$", clif_data$Name[i])){
    clif_data$Brand_1[i] <- paste(clif_data$Brand_1[i], "Minis")
  }
}
clif_data$Brand_1 <- as.factor(clif_data$Brand_1)

# Add allergen indicator columns
#  e.g.: Extracted data may pull the "may contain"
#   component sometimes (should filter for 
#   'Contains' before slicing)
clif_data$Allergens <- as.character(clif_data$Allergens)
clif_data$Dairy <- rep(NA, length(clif_data))
clif_data$Nuts <- rep(NA, length(clif_data))
clif_data$Peanuts <- rep(NA, length(clif_data))
clif_data$Soy <- rep(NA, length(clif_data))
clif_data$Wheat <- rep(NA, length(clif_data))
for(i in 1:nrow(clif_data)){
  
  # Check for milk
  clif_data$Dairy[i] <- grepl(".*milk.*", clif_data$Allergens[i])
  
  # Check for peanuts
  clif_data$Peanuts[i] <- grepl(".*peanut.*", clif_data$Allergens[i])
  
  # Check for soy
  clif_data$Soy[i] <- grepl(".*soy.*", clif_data$Allergens[i])
  
  # Check for wheat
  clif_data$Wheat[i] <- grepl(".*wheat.*", clif_data$Allergens[i])
  
  # Check for tree nuts
  clif_data$Nuts[i] <-
    (grepl(".*almond.*", clif_data$Allergens[i]) | 
       grepl(".*pecan.*", clif_data$Allergens[i]) | 
       grepl(".*cashew.*", clif_data$Allergens[i]) | 
       grepl(".*macadamia.*", clif_data$Allergens[i]) | 
       grepl(".*walnut.*", clif_data$Allergens[i]) | 
       grepl(".*coconut.*", clif_data$Allergens[i]) | 
       grepl(".*hazelnut.*", clif_data$Allergens[i]) | 
       grepl(".*tree.*", clif_data$Allergens[i]))
}

# Create a protein-only version of the data
clif_data_protein <- clif_data[complete.cases(clif_data$Protein), ]

##########
# For entries with protein called out, chart protein
##########
library(ggplot2)
library(extrafont)

# Bar chart, all protein items
#  Too long; also, faceting messes up the labels
ggplot(clif_data_protein, 
       aes(x = reorder(Name, Protein, sum), 
           y = Protein, fill = Brand_1)) +
  geom_col() + coord_flip() +
  facet_wrap(~Brand_2)

# Bar chart, high-protein, Clif items
#  Better, but brands are stacked
ggplot(clif_data_protein[clif_data_protein$Protein >= 6 & 
                           clif_data_protein$Brand_2 == "CLIF", ], 
       aes(x = reorder(Name, Protein, sum), 
           y = Protein, fill = Brand_1)) +
  geom_col() + coord_flip()

# Bar chart, Clif Bar brand only, no minis
#  Good
#font_import("Arial Black")
ggplot(clif_data_protein[(clif_data_protein$Brand_1 == "CLIF BAR"), ], 
       aes(x = reorder(Name, Protein, sum), y = Protein)) +
  geom_col(fill = 'red', color = 'black') + coord_flip() +
  labs(x = element_blank(), y = 'Protein (grams)',
       title = 'Clif Bar Protein by Variety') +
  #theme_minimal() +
  theme(axis.text.y = element_blank(),
        axis.ticks = element_blank(),
        panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(),
        panel.background = element_blank()) +
  scale_y_continuous(breaks = seq(0, 12, 1),
                     expand = c(0, 0)) +
  geom_text(aes(label = Name), hjust = 1.1, color = 'white', 
            family = "Arial Black", size = 3.5)

# Bar chart, Builders Bar brand only
#  Boring--all the same
ggplot(clif_data_protein[(clif_data_protein$Brand_1 == "BUILDERS"), ], 
       aes(x = reorder(Name, Protein, sum), y = Protein)) +
  geom_col(fill = 'red', color = 'black') + coord_flip() +
  labs(x = element_blank(), y = 'Protein (grams)',
       title = 'Clif Bar Protein by Variety') +
  theme_minimal() +
  theme(axis.text.y = element_blank()) +
  scale_y_continuous(breaks = seq(0, 10, 2),
                     expand = c(0, 0)) +
  geom_text(aes(label = Name), hjust = 1.1, 
            color = 'white', size = 3.5)
