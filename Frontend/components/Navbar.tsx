// src/components/Navbar.tsx
"use client";

import React, { useState, useContext } from "react";
import AppBar from "@mui/material/AppBar";
import Box from "@mui/material/Box";
import Toolbar from "@mui/material/Toolbar";
import IconButton from "@mui/material/IconButton";
import Typography from "@mui/material/Typography";
import Menu from "@mui/material/Menu";
import MenuItem from "@mui/material/MenuItem";
import MenuIcon from "@mui/icons-material/Menu";
import LanguageIcon from "@mui/icons-material/Language";
import Drawer from "@mui/material/Drawer";
import List from "@mui/material/List";
import ListItem from "@mui/material/ListItem";
import ListItemText from "@mui/material/ListItemText";
import Button from "@mui/material/Button";
import { useTranslation } from "react-i18next";
import { TutorialContext } from "@/context/TutorialContext";

interface NavbarProps {
  openTutorial: () => void;
}

const Navbar: React.FC<NavbarProps> = ({ openTutorial }) => {
  const { t, i18n } = useTranslation();
  const tutorialContext = useContext(TutorialContext);

  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
  const [drawerOpen, setDrawerOpen] = useState(false);

  const handleLanguageClick = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleLanguageClose = () => {
    setAnchorEl(null);
  };

  const changeLanguage = (lng: string) => {
    i18n.changeLanguage(lng);
    handleLanguageClose();
  };

  const toggleDrawer =
    (open: boolean) => (event: React.KeyboardEvent | React.MouseEvent) => {
      if (
        event.type === "keydown" &&
        ((event as React.KeyboardEvent).key === "Tab" ||
          (event as React.KeyboardEvent).key === "Shift")
      ) {
        return;
      }

      setDrawerOpen(open);
    };

  const menuItems = [
    { text: t("home"), link: "#" },
    { text: t("about"), link: "#" },
    { text: t("contact"), link: "#" },
  ];

  const drawerList = () => (
    <Box
      sx={{ width: 250 }}
      role="presentation"
      onClick={toggleDrawer(false)}
      onKeyDown={toggleDrawer(false)}
    >
      <List>
        {menuItems.map((item, index) => (
          <ListItem key={index} button component="a" href={item.link}>
            <ListItemText primary={item.text} />
          </ListItem>
        ))}
        {/* Tutorial Button in Drawer */}
        <ListItem button onClick={openTutorial}>
          <ListItemText primary={t("tutorial")} />
        </ListItem>
      </List>
    </Box>
  );

  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar
        sx={{
          height: 56,
          position: "static",
          justifyContent: "center",
        }}
      >
        <Toolbar
          disableGutters
          sx={{
            minHeight: "56px !important",
            px: 2,
          }}
        >
          <IconButton
            size="large"
            edge="start"
            color="inherit"
            aria-label="menu"
            sx={{ mr: 2, display: { xs: "flex", md: "none" } }}
            onClick={toggleDrawer(true)}
          >
            <MenuIcon />
          </IconButton>

          <Typography
            variant="h6"
            component="div"
            sx={{ flexGrow: 1, fontSize: "1.2rem", fontWeight: 500 }}
          >
            Podatki AI
          </Typography>

          <Box sx={{ display: { xs: "none", md: "flex" }, flexGrow: 1 }}>
            {menuItems.map((item, index) => (
              <Button
                key={index}
                color="inherit"
                href={item.link}
                sx={{
                  textTransform: "none",
                  fontSize: "0.95rem",
                  mx: 1,
                  "&:hover": {
                    backgroundColor: "rgba(255, 255, 255, 0.1)",
                  },
                }}
              >
                {item.text}
              </Button>
            ))}
            {/* Tutorial Button in Navbar */}
            <Button
              color="inherit"
              onClick={openTutorial}
              sx={{
                textTransform: "none",
                fontSize: "0.95rem",
                mx: 1,
                "&:hover": {
                  backgroundColor: "rgba(255, 255, 255, 0.1)",
                },
              }}
            >
              {t("tutorial")}
            </Button>
          </Box>

          {/* Language Change Icon with Ref */}
          <IconButton
            size="large"
            color="inherit"
            onClick={handleLanguageClick}
            aria-controls="language-menu"
            aria-haspopup="true"
            sx={{ ml: 1 }}
            ref={tutorialContext?.languageRef}
          >
            <LanguageIcon />
          </IconButton>
          <Menu
            id="language-menu"
            anchorEl={anchorEl}
            open={Boolean(anchorEl)}
            onClose={handleLanguageClose}
            anchorOrigin={{
              vertical: "bottom",
              horizontal: "right",
            }}
            transformOrigin={{
              vertical: "top",
              horizontal: "right",
            }}
          >
            <MenuItem onClick={() => changeLanguage("pl")}>Polski</MenuItem>
            <MenuItem onClick={() => changeLanguage("en")}>English</MenuItem>
            <MenuItem onClick={() => changeLanguage("ua")}>Українська</MenuItem>
          </Menu>
        </Toolbar>
      </AppBar>

      <Drawer anchor="left" open={drawerOpen} onClose={toggleDrawer(false)}>
        {drawerList()}
      </Drawer>
    </Box>
  );
};

export default Navbar;
