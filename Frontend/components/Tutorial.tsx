// src/components/Tutorial.tsx
"use client";

import React, { useState, useContext, useEffect, useMemo } from "react";
import {
  Popover,
  Typography,
  Button,
  Box,
  Checkbox,
  FormControlLabel,
} from "@mui/material";
import { TutorialContext } from "@/context/TutorialContext";
import { useTranslation } from "react-i18next";

interface TutorialProps {
  open: boolean;
  onClose: () => void;
}

const Tutorial: React.FC<TutorialProps> = ({ open, onClose }) => {
  const tutorialContext = useContext(TutorialContext);
  const { t } = useTranslation();

  const [step, setStep] = useState(0);
  const [anchorEl, setAnchorEl] = useState<HTMLElement | null>(null);
  const [dontShowAgain, setDontShowAgain] = useState(false);

  // Define tutorial steps
  const steps = useMemo(
    () => [
      {
        title: t("tutorial_language_title"),
        description: t("tutorial_language_description"),
        targetRef: tutorialContext?.languageRef,
      },
      {
        title: t("tutorial_chat_features_title"),
        description: t("tutorial_chat_features_description"),
        targetRef: tutorialContext?.chatInputRef,
      },
    ],
    [t, tutorialContext]
  );

  useEffect(() => {
    if (open) {
      setStep(0);
    }
  }, [open]);

  useEffect(() => {
    if (open && step < steps.length) {
      const currentStep = steps[step];
      setAnchorEl(currentStep.targetRef?.current || null);

      // Apply highlight to the current step
      currentStep.targetRef?.current?.classList.add("highlight");
      console.log(
        `Highlight added to step ${step}:`,
        currentStep.targetRef?.current
      );

      // Remove highlight from the previous step
      if (step > 0) {
        const previousStep = steps[step - 1];
        previousStep.targetRef?.current?.classList.remove("highlight");
        console.log(
          `Highlight removed from step ${step - 1}:`,
          previousStep.targetRef?.current
        );
      }
    } else if (step === steps.length) {
      // Remove highlight from the last step
      const lastStep = steps[step - 1];
      lastStep.targetRef?.current?.classList.remove("highlight");
      console.log(
        `Highlight removed from last step:`,
        lastStep.targetRef?.current
      );
    }

    // Cleanup highlights when tutorial is closed or steps change
    return () => {
      steps.forEach((s, index) => {
        s.targetRef?.current?.classList.remove("highlight");
        console.log(
          `Cleanup highlight from step ${index}:`,
          s.targetRef?.current
        );
      });
    };
  }, [step, steps, open]);

  const handleNext = () => {
    if (step < steps.length - 1) {
      setStep((prev) => prev + 1);
    } else {
      onClose();
      setStep(0);
      if (dontShowAgain) {
        // Implement logic to not show the tutorial again
        localStorage.setItem("dontShowTutorial", "true");
      }
    }
  };

  const handleClose = () => {
    onClose();
    if (step < steps.length) {
      steps[step]?.targetRef?.current?.classList.remove("highlight");
      console.log(
        `Highlight removed on close:`,
        steps[step]?.targetRef?.current
      );
    }
    setStep(0);
  };

  if (!tutorialContext) return null;

  return (
    <Popover
      open={open && step < steps.length}
      anchorEl={anchorEl}
      onClose={handleClose}
      anchorOrigin={{
        vertical: "bottom",
        horizontal: "center",
      }}
      transformOrigin={{
        vertical: "top",
        horizontal: "center",
      }}
      disableRestoreFocus
    >
      <Box sx={{ p: 2, maxWidth: 300 }}>
        <Typography variant="h6" gutterBottom>
          {steps[step].title}
        </Typography>
        <Typography variant="body1" gutterBottom>
          {steps[step].description}
        </Typography>

        <Box sx={{ display: "flex", justifyContent: "flex-end", mt: 2 }}>
          <Button variant="contained" color="primary" onClick={handleNext}>
            {step < steps.length - 1 ? t("next") : t("finish")}
          </Button>
        </Box>
      </Box>
    </Popover>
  );
};

export default Tutorial;
